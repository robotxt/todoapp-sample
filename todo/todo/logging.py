import os

debug_level = 'DEBUG'
if os.environ.get("ENVIRONMENT") == "PRODUCTION":
    debug_level = 'INFO'

DJANGO_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} ({module}) : {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': debug_level,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': debug_level,
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
    }
}
