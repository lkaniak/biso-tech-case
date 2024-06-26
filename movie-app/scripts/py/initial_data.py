import logging

from api.core.v1.movies.utils import init_db_movies
from api.core.v1.ratings.utils import init_db_ratings
from api.core.v1.users.utils import init_db_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    init_db_users()
    init_db_movies()
    init_db_ratings()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
