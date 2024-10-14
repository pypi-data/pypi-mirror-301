import logging
from typing import Optional
from .dist_util import get_dist_info

_initialized_loggers = {}


def get_root_logger(logger_name: str = 'datvtn - codeformer', log_level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Get the root logger and initialize it if it hasn't been initialized yet.

    Args:
        logger_name (str): The name of the root logger. Default is 'datvtn - codeformer'.
        log_file (str | None): If specified, a FileHandler will be added to the root logger to log to this file.
        log_level (int): The logging level. Default is `logging.INFO`. 
                         Only rank 0 process will set this log level, others will be set to "ERROR".

    Returns:
        logging.Logger: The initialized logger.
    """
    logger = logging.getLogger(logger_name)

    # Return the logger if it has already been initialized
    if logger_name in _initialized_loggers:
        return logger

    # Create format for log messages
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)

    # Add a StreamHandler (for console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # Prevent logger from propagating logs to the root logger
    logger.propagate = False

    # Get distributed training rank
    rank, _ = get_dist_info()

    if rank != 0:
        # For non-master processes, log level is set to ERROR
        logger.setLevel(logging.ERROR)
    else:
        # Set the logger level for the master process
        logger.setLevel(log_level)
        if log_file is not None:
            # Add FileHandler to log to the specified file
            file_handler = logging.FileHandler(log_file, mode='a')  # 'a' mode to append to log
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)
            logger.addHandler(file_handler)

    # Mark logger as initialized
    _initialized_loggers[logger_name] = True

    return logger
