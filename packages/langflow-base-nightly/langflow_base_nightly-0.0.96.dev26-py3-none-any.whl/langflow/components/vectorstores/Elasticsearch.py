from typing import Any

from langchain.schema import Document
from langchain_elasticsearch import ElasticsearchStore
from loguru import logger

from langflow.base.vectorstores.model import LCVectorStoreComponent, check_cached_vector_store
from langflow.io import (
    DataInput,
    DropdownInput,
    FloatInput,
    HandleInput,
    IntInput,
    MultilineInput,
    SecretStrInput,
    StrInput,
)
from langflow.schema import Data


class ElasticsearchVectorStoreComponent(LCVectorStoreComponent):
    """
    Elasticsearch Vector Store with with advanced, customizable search capabilities.
    """

    display_name: str = "Elasticsearch"
    description: str = "Elasticsearch Vector Store with with advanced, customizable search capabilities."
    documentation = "https://python.langchain.com/docs/integrations/vectorstores/elasticsearch"
    name = "Elasticsearch"
    icon = "ElasticsearchStore"

    inputs = [
        StrInput(
            name="elasticsearch_url",
            display_name="Elasticsearch URL",
            value="http://localhost:9200",
            info="URL for self-managed Elasticsearch deployments (e.g., http://localhost:9200). "
            "Do not use with Elastic Cloud deployments, use Elastic Cloud ID instead.",
        ),
        SecretStrInput(
            name="cloud_id",
            display_name="Elastic Cloud ID",
            value="",
            info="Use this for Elastic Cloud deployments. Do not use together with 'Elasticsearch URL'.",
        ),
        StrInput(
            name="index_name",
            display_name="Index Name",
            value="langflow",
            info="The index name where the vectors will be stored in Elasticsearch cluster.",
        ),
        MultilineInput(
            name="search_input",
            display_name="Search Input",
            info="Enter a search query. Leave empty to retrieve all documents.",
        ),
        StrInput(
            name="username",
            display_name="Username",
            value="",
            advanced=False,
            info=(
                "Elasticsearch username (e.g., 'elastic'). "
                "Required for both local and Elastic Cloud setups unless API keys are used."
            ),
        ),
        SecretStrInput(
            name="password",
            display_name="Password",
            value="",
            advanced=False,
            info=(
                "Elasticsearch password for the specified user. "
                "Required for both local and Elastic Cloud setups unless API keys are used."
            ),
        ),
        DataInput(
            name="ingest_data",
            display_name="Ingest Data",
            is_list=True,
        ),
        HandleInput(
            name="embedding",
            display_name="Embedding",
            input_types=["Embeddings"],
        ),
        DropdownInput(
            name="search_type",
            display_name="Search Type",
            options=["similarity", "mmr"],
            value="similarity",
            advanced=True,
        ),
        IntInput(
            name="number_of_results",
            display_name="Number of Results",
            info="Number of results to return.",
            advanced=True,
            value=4,
        ),
        FloatInput(
            name="search_score_threshold",
            display_name="Search Score Threshold",
            info="Minimum similarity score threshold for search results.",
            value=0.0,
            advanced=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="Elastic API Key",
            value="",
            advanced=True,
            info="API Key for Elastic Cloud authentication. If used, 'username' and 'password' are not required.",
        ),
    ]

    @check_cached_vector_store
    def build_vector_store(self) -> ElasticsearchStore:
        """
        Builds the Elasticsearch Vector Store object.
        """
        if self.cloud_id and self.elasticsearch_url:
            msg = (
                "Both 'cloud_id' and 'elasticsearch_url' provided. "
                "Please use only one based on your deployment (Cloud or Local)."
            )
            raise ValueError(msg)

        es_params = {
            "index_name": self.index_name,
            "embedding": self.embedding,
            "es_user": self.username if self.username else None,
            "es_password": self.password if self.password else None,
        }

        if self.cloud_id:
            es_params["es_cloud_id"] = self.cloud_id
        else:
            es_params["es_url"] = self.elasticsearch_url

        if self.api_key:
            es_params["api_key"] = self.api_key

        elasticsearch = ElasticsearchStore(**es_params)

        # If documents are provided, add them to the store
        if self.ingest_data:
            documents = self._prepare_documents()
            if documents:
                elasticsearch.add_documents(documents)

        return elasticsearch

    def _prepare_documents(self) -> list[Document]:
        """
        Prepares documents from the input data to add to the vector store.
        """
        documents = []
        for data in self.ingest_data:
            if isinstance(data, Data):
                documents.append(data.to_lc_document())
            else:
                error_message = "Vector Store Inputs must be Data objects."
                logger.error(error_message)
                raise ValueError(error_message)
        return documents

    def _add_documents_to_vector_store(self, vector_store: "ElasticsearchStore") -> None:
        """
        Adds documents to the Vector Store.
        """
        documents = self._prepare_documents()
        if documents and self.embedding:
            logger.debug(f"Adding {len(documents)} documents to the Vector Store.")
            vector_store.add_documents(documents)
        else:
            logger.debug("No documents to add to the Vector Store.")

    def search(self, query: str | None = None) -> list[dict[str, Any]]:
        """
        Search for similar documents in the vector store or retrieve all documents
        if no query is provided.
        """
        vector_store = self.build_vector_store()
        search_kwargs = {
            "k": self.number_of_results,
            "score_threshold": self.search_score_threshold,
        }

        if query:
            search_type = self.search_type.lower()
            try:
                if search_type == "similarity":
                    results = vector_store.similarity_search_with_score(query, **search_kwargs)
                elif search_type == "mmr":
                    results = vector_store.max_marginal_relevance_search(query, **search_kwargs)
                else:
                    msg = f"Invalid search type: {self.search_type}"
                    raise ValueError(msg)
            except Exception as e:
                msg = (
                    "Error occurred while querying the Elasticsearch VectorStore,"
                    " there is no Data into the VectorStore."
                )
                logger.exception(msg)
                raise ValueError(msg) from e
            return [
                {"page_content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results
            ]
        results = self.get_all_documents(vector_store, **search_kwargs)
        return [{"page_content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results]

    def get_all_documents(self, vector_store: ElasticsearchStore, **kwargs) -> list[tuple[Document, float]]:
        """
        Retrieve all documents from the vector store.
        """
        client = vector_store.client
        index_name = self.index_name

        query = {
            "query": {"match_all": {}},
            "size": kwargs.get("k", self.number_of_results),
        }

        response = client.search(index=index_name, body=query)

        results = []
        for hit in response["hits"]["hits"]:
            doc = Document(
                page_content=hit["_source"].get("text", ""),
                metadata=hit["_source"].get("metadata", {}),
            )
            score = hit["_score"]
            results.append((doc, score))

        return results

    def search_documents(self) -> list[Data]:
        """
        Search for documents in the vector store based on the search input.
        If no search input is provided, retrieve all documents.
        """
        results = self.search(self.search_input)
        retrieved_data = [
            Data(
                text=result["page_content"],
                file_path=result["metadata"].get("file_path", ""),
            )
            for result in results
        ]
        self.status = retrieved_data
        return retrieved_data

    def get_retriever_kwargs(self):
        """
        Get the keyword arguments for the retriever.
        """
        return {
            "search_type": self.search_type.lower(),
            "search_kwargs": {
                "k": self.number_of_results,
                "score_threshold": self.search_score_threshold,
            },
        }
