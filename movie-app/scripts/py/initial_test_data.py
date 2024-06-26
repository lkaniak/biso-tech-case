import logging

import api.core

print(api.core)
from api.core.v1.users.utils import init_test_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    init_test_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
