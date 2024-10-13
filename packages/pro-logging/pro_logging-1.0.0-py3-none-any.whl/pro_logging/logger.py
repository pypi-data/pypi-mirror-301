# logger.py

import os
import json
import sqlite3
from datetime import datetime
import shutil

class AdvancedLogger:
    """
    A logger class that logs messages to both a file and optionally a database.
    Supports log rotation, JSON formatting, and different log levels.
    """
    def __init__(self, log_filename='logfile.log', level="INFO", log_to_console=True, max_size_mb=5, rotate_logs=False, date_based_rotation=False, json_format=False, db_path=None):
        """
        Initialize the logger with optional parameters for file name, log level, console output,
        log rotation, and JSON formatting.
        """
        self.log_filename = log_filename
        self.level = level
        self.log_to_console = log_to_console
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.rotate_logs = rotate_logs
        self.date_based_rotation = date_based_rotation
        self.json_format = json_format
        self.db_path = db_path
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.logfile = os.path.join(self.project_dir, self.log_filename)

        # Log levels
        self.levels = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }

        if self.db_path:
            self._init_db()

    def _init_db(self):
        """Create a logs table in the database if it doesn't already exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                message TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _rotate_logs(self):
        """Handle log rotation based on file size or date."""
        if self.date_based_rotation:
            new_logfile = f"{self.logfile}_{datetime.now().strftime('%Y-%m-%d')}"
            shutil.move(self.logfile, new_logfile)
        else:
            if os.path.exists(self.logfile) and os.path.getsize(self.logfile) >= self.max_size_bytes:
                new_logfile = f"{self.logfile}.1"
                shutil.move(self.logfile, new_logfile)

    def _log_to_console(self, message):
        """Print the log message to the console."""
        print(message)

    def _log_to_file(self, message):
        """Write the log message to the log file."""
        with open(self.logfile, 'a') as log_file:
            log_file.write(message + '\n')

    def _log_to_db(self, message, level):
        """Insert the log message into the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)", (timestamp, level, message))
        conn.commit()
        conn.close()

    def log(self, message, level="INFO"):
        """
        Log a message with the specified level.
        The message is logged to the console, file, and database (if applicable).
        """
        if self.levels.get(level, 20) < self.levels.get(self.level, 20):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.json_format:
            log_message = json.dumps({
                "timestamp": timestamp,
                "level": level,
                "message": message
            })
        else:
            log_message = f"[{timestamp}] [{level}] {message}"

        if self.rotate_logs:
            self._rotate_logs()

        self._log_to_file(log_message)

        if self.db_path:
            self._log_to_db(message, level)

        if self.log_to_console:
            self._log_to_console(log_message)

    def log_debug(self, message):
        """Log a message at the DEBUG level."""
        self.log(message, "DEBUG")

    def log_info(self, message):
        """Log a message at the INFO level."""
        self.log(message, "INFO")

    def log_warning(self, message):
        """Log a message at the WARNING level."""
        self.log(message, "WARNING")

    def log_error(self, message):
        """Log a message at the ERROR level."""
        self.log(message, "ERROR")

    def log_critical(self, message):
        """Log a message at the CRITICAL level."""
        self.log(message, "CRITICAL")

    def log_start(self):
        """Log the start of a process."""
        self.log("Process started.", "INFO")

    def log_end(self):
        """Log the end of a process."""
        self.log("Process ended.", "INFO")

    def set_level(self, level):
        """
        Set the log level for the logger.
        Only messages with a level equal to or higher than this will be logged.
        """
        if level in self.levels:
            self.level = level
        else:
            raise ValueError("Invalid log level. Choose from DEBUG, INFO, WARNING, ERROR, CRITICAL.")
