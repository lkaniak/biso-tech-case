import logging

from api.core.v1.recommendation.ml.feature_engineering.training import (
    training_feature_engineering,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Generating model")
    training_feature_engineering()
    logger.info("model created")


if __name__ == "__main__":
    main()
