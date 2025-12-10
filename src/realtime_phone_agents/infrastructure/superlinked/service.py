from typing import Any

import pandas as pd
from loguru import logger
from superlinked import framework as sl

from realtime_phone_agents.config import settings
from realtime_phone_agents.infrastructure.superlinked.index import (
    property_index,
    property_schema,
)
from realtime_phone_agents.infrastructure.superlinked.query import property_search_query


class PropertySearchService:
    """Service for searching properties using Superlinked."""

    def __init__(
        self,
        qdrant_host: str | None,
        qdrant_port: int | None,
        qdrant_api_key: str | None,
        qdrant_cluster_url: str | None,
        qdrant_use_cloud: bool | None,
    ):
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_cluster_url = qdrant_cluster_url
        self.qdrant_use_cloud = qdrant_use_cloud

        self.app = None
        self.source = None

        # Setup the application
        self._setup_app()

    def _setup_app(self):
        """Setup  the Superlinked application with RestExecutor and Qdrant, fallback to InMemoryExecutor"""
        try:
            self._setup_with_qdrant()
        except Exception as e:
            logger.warning(
                f"Qdrant setup failed, falling back to InMemoryExecutor: {e}"
            )
            self._setup_with_memmory()

    def _setup_with_qdrant(self):
        """Setup the Superlinked application with RestExecutor and Qdrant"""
        protocol = "https" if self.qdrant_use_cloud else "http"

        if self.qdrant_use_cloud:
            qdrant_url = f"{self.qdrant_cluster_url}:{self.qdrant_port}"
        else:
            qdrant_url = f"{protocol}://{self.qdrant_host}:{self.qdrant_port}"

        vector_db = sl.QdrantVectorDatabase(
            url=qdrant_url,
            api_key=self.qdrant_api_key,
            default_query_limit=3,
        )

        logger.info(f"Connecting to Qdrant at {qdrant_url} ...")

        self.source = sl.RestSource(
            property_schema, parser=sl.DataFrameParser(schema=property_schema)
        )

        search_descriptor = sl.RestDescriptor(query_path="/search")
        rest_query = sl.RestQuery(search_descriptor, property_search_query)

        executor = sl.RestExecutor(
            sources=[self.source],
            indices=[property_index],
            queries=[rest_query],
            vector_database=vector_db,
        )

        self.app = executor.run()

        logger.info("PropertySearchService initialized with Qdrant RestExecutor")

    def _setup_with_memmory(self):
        """Setup the Superlinked application with InMemoryExecutor"""

        self.source = sl.InMemorySource(
            property_schema, parser=sl.DataFrameParser(schema=property_schema)
        )

        executor = sl.InMemoryExecutor(
            sources=[self.source],
            indices=[property_index],
        )
        self.app = executor.run()

        logger.info("PropertySearchService initialized with InMemoryExecutor")

    def ingest_properties(self, properties_data_path: str):
        """Ingest properties from a CSV file into the Superlinked application"""

        logger.info(f"Ingesting properties from {properties_data_path} ...")
        df = pd.read_csv(properties_data_path)

        self.source.put([df])
        logger.info(f"Ingested {len(df)} properties")

    def _result_to_properties(self, result) -> list[dict[str, Any]]:
        """Convert QueryResult to clean property dicts by extracting entries and merging id into fields."""
        entries = result.model_dump()["entries"]
        return [{**entry["fields"], "id": int(entry["id"])} for entry in entries]

    async def search_properties(self, query: str, limit: int = 1):
        """Search for properties using semantic search and natural queries"""
        try:
            results = await self.app.async_query(
                property_search_query, natural_query=query, limit=limit
            )
            properties = self._result_to_properties(results)

            if not properties:
                logger.warning(f"Properties for query '{query}' not found")
                return []

            return properties
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []


# Global service instance
_property_service = None


def get_property_search_service(
    qdrant_host: str | None = settings.qdrant.host,
    qdrant_port: int | None = settings.qdrant.port,
    qdrant_api_key: str | None = settings.qdrant.api_key,
    qdrant_cluster_url: str | None = settings.qdrant.cluster_url,
    qdrant_use_cloud: bool | None = settings.qdrant.use_qdrant_cloud,
) -> PropertySearchService:
    """Get or create the global property search service instance."""
    global _property_service
    if _property_service is None:
        _property_service = PropertySearchService(
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port,
            qdrant_api_key=qdrant_api_key,
            qdrant_cluster_url=qdrant_cluster_url,
            qdrant_use_cloud=qdrant_use_cloud,
        )
    return _property_service
