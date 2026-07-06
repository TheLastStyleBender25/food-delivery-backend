import logging

logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(name)s - "
        "%(filename)s:%(lineno)d - "
        "%(message)s"
    ))

logger = logging.getLogger("restaurant_service_logger")