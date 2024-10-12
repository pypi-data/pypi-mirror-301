from __future__ import annotations

import logging
import os


class Logger:
    def __init__(
            self,
            name: str,
            level: str = 'DEBUG',
            include_in: list[str] | tuple[str] | None = None,
            files_before_archiving: int = 360,
            propagate: bool = False,
    ):
        self.name = name
        self.level = level
        self.include_in = include_in or []
        self.files_before_archiving = files_before_archiving
        self.propagate = propagate


class LoggingBuilder:
    def __init__(
            self,
            logs_dir: str,
            loggers: list[Logger, ...] | tuple[Logger, ...],
            format: str = '{levelname} {asctime}: {message}',
            datefmt: str = '%d-%m %H:%M:%S'
    ):
        self.logs_dir = logs_dir
        self.format = format
        self.datefmt = datefmt
        self.loggers = loggers

    @staticmethod
    def check_loggers(LOGGING: dict) -> None:
        if os.environ.get('RUN_MAIN') != 'true':
            for logger_name in LOGGING['loggers']:
                log = logging.getLogger(logger_name)
                log.warning(f'Logger found: {logger_name}')

    def build(self) -> dict:
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'base_formatter': {
                    'format': self.format,
                    'style': '{',
                    'datefmt': self.datefmt,
                }
            },
            'handlers': {},
            'loggers': {}
        }

        # Create logs directory
        os.makedirs(self.logs_dir, exist_ok=True)
        LOGGING['handlers']['console'] = {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'base_formatter',
        }

        # Mapping from logger name to its file handler name
        logger_name_to_file_handler_name = {}

        # First, create file handlers for each logger
        for logger in self.loggers:
            logger_name = logger.name
            log_dir = os.path.join(self.logs_dir, logger_name)
            os.makedirs(log_dir, exist_ok=True)

            log_file_handler_name = f'{logger_name}_file'
            logger_name_to_file_handler_name[logger_name] = log_file_handler_name
            LOGGING['handlers'][log_file_handler_name] = {
                'level': logger.level,
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(log_dir, f'{logger_name}.log'),
                'when': 'midnight',
                'backupCount': logger.files_before_archiving,
                'formatter': 'base_formatter',
                'encoding': 'utf-8',
                'delay': True,
            }

            # Initialize logger configuration
            LOGGING['loggers'][logger_name] = {
                'handlers': [],  # We'll fill this in the next loop
                'level': logger.level,
                'propagate': logger.propagate,
            }

        # Create global_file handler if not already created
        if 'global_file' not in LOGGING['handlers']:
            global_log_dir = os.path.join(self.logs_dir, 'global')
            os.makedirs(global_log_dir, exist_ok=True)
            LOGGING['handlers']['global_file'] = {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(global_log_dir, 'global.log'),
                'when': 'midnight',
                'backupCount': 360,
                'formatter': 'base_formatter',
                'encoding': 'utf-8',
                'delay': True,
            }
            # Ensure the global logger has its own handler and console
            LOGGING['loggers']['global'] = {
                'handlers': [
                    'console',
                    'global_file'
                ],
                'level': 'DEBUG',
                'propagate': False,
            }

        # Now, assign handlers to each logger
        for logger in self.loggers:
            logger_name = logger.name
            handler_names = ['console', logger_name_to_file_handler_name[logger_name]]

            # Add global_file handler to all loggers except 'global' itself
            if logger_name != 'global':
                handler_names.append('global_file')

            # Add file handlers from include_in loggers
            for include_logger in logger.include_in:
                if include_logger in logger_name_to_file_handler_name:
                    include_handler_name = logger_name_to_file_handler_name[include_logger]
                    handler_names.append(include_handler_name)
                else:
                    # Handle the case where the included logger is not defined
                    raise ValueError(f"Included logger '{include_logger}' for logger '{logger_name}' is not defined.")

            # Remove duplicates
            handler_names = list(set(handler_names))

            LOGGING['loggers'][logger_name]['handlers'] = handler_names

        return LOGGING
