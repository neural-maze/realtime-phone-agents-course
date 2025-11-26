from superlinked import framework as sl

from realtime_phone_agents.config import settings
from realtime_phone_agents.infrastructure.superlinked.index import property_index, property_schema, description_space, size_space, price_space
from realtime_phone_agents.infrastructure.superlinked.constants import NEIGHBORHOODS


openai_config = sl.OpenAIClientConfig(
    api_key=settings.openai.api_key, model=settings.openai.model
)

property_search_query = (
    sl.Query(
        property_index,
        weights={
            description_space: sl.Param("description_weight"),
            size_space: sl.Param("size_weight"),
            price_space: sl.Param("price_weight"),
        },
    )
    .find(property_schema)
    .with_natural_query(sl.Param("natural_query"), openai_config)
    .similar(
        description_space,
        sl.Param(
            "description_query",
            description="The user's natural language query for property search.",
        ),
    )
    .filter(
        property_schema.location 
        == sl.Param(
            "location",
            description="Used to filter appartments by neighborhood",
            options=NEIGHBORHOODS
        ))
    .filter(
        property_schema.rooms 
        >= sl.Param(
            "min_rooms",
            description="Used to find apartments with a room count equal to or greater than the specified number"
        ))
    .filter(
        property_schema.baths 
        >= sl.Param(
            "min_baths",
            description="Used to find apartments with a bath count equal to or greater than the specified number"
        ))
    .filter(
        property_schema.sqft 
        >= sl.Param(
            "sqft_bigger_than",
            description="Used to find appartments with square feet equal to or greather than the specified number"
        ))
    .filter(
        property_schema.price 
        <= sl.Param(
            "price_smaller_than",
            description="Used to find appartments with price less than the specified number"
        ))
    .limit(sl.Param("limit"))
    .select_all()
)
