import logging

def get_logger(name="camera_movement_logger"):
    """
    Creates and returns a logger with both console and file handlers.

    This function sets up a logger with two handlers:
    1. A console handler that logs debug and higher level messages to the console.
    2. A file handler that logs warning and higher level messages to a log file ('logs/app.log').

    Args:
        name (str): The name of the logger (default is "camera_movement_logger").

    Returns:
        logging.Logger: A logger instance with the specified handlers.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG) 

        # Console handler for logging to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)  
        ch_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

        # File handler for logging to a file
        fh = logging.FileHandler('logs/app.log')
        fh.setLevel(logging.WARNING) 
        fh_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger
