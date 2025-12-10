from loguru import logger
from realtime_phone_agents.observability.opik_utils import configure
from realtime_phone_agents.avatars.registry import register_all_avatars, version_all_avatars

configure()

logger.info("Registering all avatars")
register_all_avatars()

logger.info("Versioning all avatars")
version_all_avatars()

logger.info("All avatars registered and versioned")
