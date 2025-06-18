import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """ 
    Sets up logging for the application.
    This function configures two separate loggers:
    1. `access_logger`: For access logs (e.g., HTTP requests).
    2. `error_logger`: For error logs (e.g., exceptions).
    It also configures a root logger for general application logs.
    """

    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Define log file paths
    access_log_path = os.path.join(logs_dir, 'access.log')
    error_log_path = os.path.join(logs_dir, 'error.log')

    # Define the log format
    # The format string uses standard logging attributes:
    # %(asctime)s: Timestamp (YYYY-MM-DD HH:MM:SS,ms)
    # %(levelname)s: Log level (e.g., INFO, WARNING, ERROR)
    # %(name)s: Logger name (e.g., 'uvicorn', 'app.api.v1.endpoints.users')
    # %(thread)d: Thread ID
    # %(message)s: The actual log message
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(thread)d - %(message)s'
    formatter = logging.Formatter(log_format)

    # --- Access Logger Setup ---
    access_logger = logging.getLogger('access_logger')
    # Access logs typically INFO or higher
    access_logger.setLevel(logging.INFO)

    # File handler for access logs (rotate at 2MB, keep 10 backups)
    access_file_handler = RotatingFileHandler(
        access_log_path,
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=10
    )
    access_file_handler.setFormatter(formatter)
    access_logger.addHandler(access_file_handler)

    # Optional: Stream handler for access logs (to console)
    access_stream_handler = logging.StreamHandler()
    access_stream_handler.setFormatter(formatter)
    access_logger.addHandler(access_stream_handler)

    # --- Error Logger Setup ---
    error_logger = logging.getLogger('error_logger')
    # Error logs typically ERROR or CRITICAL
    error_logger.setLevel(logging.ERROR)

    # File handler for error logs (rotate at 5MB, keep 10 backups)
    error_file_handler = RotatingFileHandler(
        error_log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=10
    )
    error_file_handler.setFormatter(formatter)
    error_logger.addHandler(error_file_handler)

    # Optional: Stream handler for error logs (to console)
    error_stream_handler = logging.StreamHandler()
    error_stream_handler.setFormatter(formatter)
    error_logger.addHandler(error_stream_handler)

    # --- Root Logger / Application Logger Setup ---
    # This is for general application logs that aren't strictly access or error,
    # or for logs that should go to both.
    # We'll stick to a default simple setup for the root/app logger.
    # Uvicorn also has its own loggers, which we'll address in main.py.

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Default level for general app logs

    # Clear existing handlers from root logger (important if FastAPI/Uvicorn adds them automatically)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add a stream handler for general application logs to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # You could also add a file handler for general app logs if needed
    # app_file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), maxBytes=1024*1024, backupCount=5)
    # app_file_handler.setFormatter(formatter)
    # root_logger.addHandler(app_file_handler)


setup_logging()

# Use these loggers in other parts of the application
access_logger = logging.getLogger('access_logger')
error_logger = logging.getLogger('error_logger')
app_logger = logging.getLogger(__name__)
