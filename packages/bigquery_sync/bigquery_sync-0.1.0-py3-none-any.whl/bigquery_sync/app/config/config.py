RETRY_COUNT = 3

SCHEDULED_QUERIES = '_scheduled_queries'

DO_NOT_FETCH = {
    'ata-analytics': {
        'narwhal_store_data': True,
        'narwhal_google_ads': True,
    },
}

DEFAULT_SCHEDULED_CONFIG_JSON = {
    "configuration": {
        "schedule": {
            "repeat": {
                "hourly": 24,
                "weekly": None,
                "monthly": None
            },
            "time": {
                "hour": 0,
                "minute": 30
            }
        },
        "destination": {
            "dataset": "",
            "table": None
        },
        "write_mode": None
    }
}
