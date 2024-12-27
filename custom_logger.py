import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """
    Set up a logger with a rotating file handler.
    :param name: Logger name
    :param log_file: File to write logs
    :param level: Logging level
    :return: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add the handler to the logger
    if not logger.handlers:  # Avoid adding multiple handlers
        logger.addHandler(handler)
    
    return logger
