import logging

logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(name)s - "
        "%(filename)s:%(lineno)d - "
        "%(message)s"
    ))

logger = logging.getLogger('menu_service_logger')