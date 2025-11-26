from realtime_phone_agents.agent.fastrtc_agent import FastRTCAgent
from realtime_phone_agents.agent.tools.property_search import search_property_tool
from realtime_phone_agents.infrastructure.superlinked.service import get_property_search_service

property_search_service = get_property_search_service()
property_search_service.ingest_properties("./data/properties.csv")

agent = FastRTCAgent(
    tools=[search_property_tool],
)

agent.stream.ui.launch()
