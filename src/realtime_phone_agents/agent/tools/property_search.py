import json
from langchain.tools import tool
from realtime_phone_agents.infrastructure.superlinked.service import get_property_search_service


@tool
def search_property_mock_tool(location: str) -> str:
    """Retrieve real estate details for properties in a given location."""
    return (
        "I found one apartment in that area. It features 3 rooms, "
        "2 bathrooms, and a beautifully designed living room."
    )

@tool
async def search_property_tool(query: str, limit: int = 1) -> str:
    """Search for real estate properties using natural language queries.
    
    This tool performs semantic search over a property database, allowing you to find
    properties based on user requirements like location, price, bedrooms, amenities, and more.
    The search understands natural language and can handle complex queries with multiple criteria.
    
    Examples of good queries:
        - "3 bedroom house in downtown under 500k"
        - "apartment with pool near beach, 2 bedrooms"
        - "modern condo in San Francisco with parking"
        - "family home with large backyard, good schools"
    
    Args:
        query: Natural language description of the property requirements. Can include
               location, price range, number of bedrooms/bathrooms, amenities,
               property type, and other features.
        limit: Maximum number of matching properties to return (default: 1).
               Use higher values when the user wants to compare multiple options.
    
    Returns:
        A formatted string containing details of matching properties, including:
        address, price, bedrooms, bathrooms, square footage, and key features.
        Returns an empty or error message if no properties match the criteria.
    """
    property_search_service = get_property_search_service()
    properties = await property_search_service.search_properties(query, limit)

    if not properties:
        return "No properties found matching the criteria."
    
    return json.dumps(properties, indent=2)
