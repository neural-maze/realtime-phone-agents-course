import os

import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator

from realtime_phone_agents.config import settings


def configure() -> None:
    if settings.opik.api_key and settings.opik.project_name:
        try:
            client = OpikConfigurator(api_key=settings.opik.api_key)
            default_workspace = client._get_default_workspace()
        except Exception:
            logger.warning(
                "Default workspace not found. Setting workspace to None and enabling interactive mode."
            )
            default_workspace = None

        os.environ["OPIK_PROJECT_NAME"] = settings.opik.project_name

        try:
            opik.configure(
                api_key=settings.opik.api_key,
                workspace=default_workspace,
                use_local=False,
                force=True,
            )
            logger.info(
                f"Opik configured successfully using workspace '{default_workspace}'"
            )
        except Exception:
            logger.warning(
                "Couldn't configure Opik. There is probably a problem with the OPIK_API_KEY or OPIK_PROJECT_NAME environment variables or with the Opik server."
            )
    else:
        logger.warning(
            "OPIK_API_KEY and OPIK_PROJECT_NAME are not set. Set them to enable prompt monitoring with Opik."
        )
