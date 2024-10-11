import logging

logging_format = "%(message)s"
logging.basicConfig(format=logging_format)
logger = logging.getLogger("piiip")
logger.setLevel(logging.INFO)
