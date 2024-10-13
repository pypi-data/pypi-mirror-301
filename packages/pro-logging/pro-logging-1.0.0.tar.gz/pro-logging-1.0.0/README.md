# Pro Logging

**Pro Logging** is an advanced, fully customizable logging package for Python projects. It allows developers to log their application's processes to both a log file and an optional database. This package supports various features such as log rotation, different log levels, JSON format logging, and database storage.

## Features

- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Supports both file size-based and date-based log rotation
- **JSON Format**: Option to log messages in JSON format
- **Database Logging**: Store logs in an SQLite database for easier management and analysis
- **Console Output**: Print log messages to the console
- **Customization**: Users can configure log file name, log levels, rotation settings, and more

## Installation

Install the package using pip:

```bash
pip install pro-logging
```

## Usage

Here's a basic example of how to use the pro-logging package:

```python
from pro_logging import AdvancedLogger

# Initialize the logger
logger = AdvancedLogger(
    log_filename='app.log',  # Log file name
    level="DEBUG",           # Log level
    log_to_console=True,     # Output to console
    rotate_logs=True,        # Enable log rotation
    max_size_mb=10,          # Maximum log file size before rotation
    json_format=True,        # Log in JSON format
    db_path='app_logs.db'    # Path to the SQLite database for logs
)

# Log some messages
logger.log_info("This is an informational message.")
logger.log_error("This is an error message.")
logger.log_debug("This is a debug message.")
```

## Example

Logging with Different Levels

```python
logger.log_debug("Debugging the application")
logger.log_info("Application is running")
logger.log_warning("This is a warning")
logger.log_error("An error occurred")
logger.log_critical("Critical system failure")
```

## Log Rotation

You can rotate logs based on file size or date.

```python
# Enable file size-based log rotation
logger = AdvancedLogger(rotate_logs=True, max_size_mb=5)

# Enable date-based log rotation
logger = AdvancedLogger(date_based_rotation=True)
```

## Database Logging

Logs can also be stored in an SQLite database for further analysis.

```python
logger = AdvancedLogger(db_path='app_logs.db')

# Log messages will be saved in the database
logger.log_info("This log is saved in the database as well.")
```

## Customization

You can adjust log settings such as file name, log level, JSON formatting, and more:

```python
logger = AdvancedLogger(
    log_filename='custom.log',
    level="WARNING",
    json_format=True
)
```