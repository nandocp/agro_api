import json
import logging

# import sys
from datetime import datetime
from logging.config import dictConfig

from config.settings import settings


# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'line': record.lineno,
            'message': record.getMessage()
        }

        # Add exception info if available
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)


defaul_formatter = {
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': defaul_formatter,
        'json': {
            '()': JsonFormatter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': settings.LOG_LEVEL,
            'formatter': 'json',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'fastapi.log',
            'mode': 'a'
        },
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'fastapi.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
        'time_rotating_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'fastapi.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
}

dictConfig(log_config)

logger = logging.getLogger('app')
