"""
Script to ingest properties data into Qdrant Cloud using PropertySearchService.

This script loads property data from a CSV file and ingests it into Qdrant
using the Superlinked framework for semantic search capabilities.
"""

from pathlib import Path

from loguru import logger

from realtime_phone_agents.infrastructure.superlinked.service import (
    get_property_search_service,
)


def main():
    """Main function to ingest properties into Qdrant Cloud."""
    
    # Get the path to the properties CSV file
    project_root = Path(__file__).parent.parent
    properties_data_path = project_root / "data" / "properties.csv"
    
    if not properties_data_path.exists():
        logger.error(f"Properties file not found at: {properties_data_path}")
        return
    
    logger.info("Initializing PropertySearchService...")
    
    # Get the property search service instance
    # This will use Qdrant Cloud if configured in settings
    service = get_property_search_service()
    
    logger.info(f"Starting property ingestion from {properties_data_path}")
    
    # Ingest properties from CSV file
    service.ingest_properties(str(properties_data_path))
    
    logger.success("✅ Property ingestion completed successfully!")
    logger.info("Properties are now available for semantic search in Qdrant Cloud")


if __name__ == "__main__":
    main()

