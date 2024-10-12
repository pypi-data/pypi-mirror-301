import chromadb
from chromadb.api.types import OneOrMany
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma as LangChainChroma
from ally_ai_core import Settings
from ally_ai_langchain import EmbeddingModel
from typing import Optional
import logging

from ally_ai_core.Decorators import logstep


class Chroma(LangChainChroma):
    """
    Interited from LangChain Chroma
    """

    ally_settings: Settings = None

    def __init__(
        self,
        settings: Optional[Settings] = None,
        embeddingModel: Optional[EmbeddingModel] = None,
        **kwargs,
    ) -> None:

        if settings is None:
            settings = Settings(section="chromadb")
        if embeddingModel is None:
            embeddingModel = EmbeddingModel()

        self.ally_settings = settings
        persist_directory = (
            settings.pop("persist_directory")
            if "persist_directory" in settings
            else None
        )

        if persist_directory is not None and persist_directory:
            self._init_persist_directory(embeddingModel, persist_directory, **kwargs)
        else:
            self._init_http_client(settings, embeddingModel, **kwargs)

    @logstep(message="Chroma-Init-PersistDir")
    def _init_persist_directory(self, embeddingModel, persist_directory, **kwargs):
        super().__init__(
            persist_directory=persist_directory,
            embedding_function=embeddingModel,
            create_collection_if_not_exists=False,
            **kwargs,
        )

    @logstep(message="Chroma-Init-HttpClient")
    def _init_http_client(self, settings, embeddingModel, **kwargs):
        chroma_client = chromadb.HttpClient(
            **settings, settings=ChromaSettings(anonymized_telemetry=False)
        )
        super().__init__(
            client=chroma_client,
            embedding_function=embeddingModel,
            create_collection_if_not_exists=False,
            **kwargs,
        )

    def query(
        self,
        query_texts: Optional[OneOrMany[str]] = None,
        n_results: int = 10,
        include: chromadb.Include = ["metadatas", "documents", "distances"],
    ):

        query_embeddings = [
            self._embedding_function.embed_query(query_text)
            for query_text in query_texts
        ]

        return self._collection.query(
            query_embeddings=query_embeddings, n_results=n_results, include=include
        )
