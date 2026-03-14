import json
import logging
from datetime import datetime, timezone

from config.settings import settings


# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'environment': settings.ENVIRONMENT,
        }

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        if record.stack_info:
            log_record['stack_info'] = record.stack_info

        return json.dumps(log_record)


default_formatter = {
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': default_formatter,
        'json': {'()': JsonFormatter},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': settings.LOG_LEVEL,
            'formatter': 'json',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': settings.LOG_LEVEL,
            'formatter': 'json',
            'filename': 'fastapi.log',
            'mode': 'a',
        },
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': settings.LOG_LEVEL,
            'formatter': 'json',
            'filename': 'fastapi.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
        'time_rotating_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': settings.LOG_LEVEL,
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
            'level': settings.LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {'handlers': ['console'], 'level': settings.LOG_LEVEL},
}

logger = logging.getLogger('app')
