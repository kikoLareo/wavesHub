# logging_config.py
import logging
import sys

class TransactionIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "transaction_id"):
            record.transaction_id = "N/A"  # Valor predeterminado si falta
        return True

# Configuración de logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - [ID: %(transaction_id)s] - %(message)s",
            "defaults": {"transaction_id": "N/A"},  # Añadir un valor predeterminado
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Función para configurar el logging
def setup_logging():
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger()
    logger.addFilter(TransactionIDFilter())

