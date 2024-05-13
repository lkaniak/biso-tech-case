import logging

from src.core.v1.movies.utils import init_db_movies
from src.core.v1.users.utils import init_db_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    init_db_users()
    init_db_movies()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
