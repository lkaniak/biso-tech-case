import logging

from src.core.v1.users.utils import init_db_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    init_db_users()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
