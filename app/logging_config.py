import logging
import sys
import logging.config

class TransactionIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "transaction_id"):
            record.transaction_id = "N/A"  # Valor predeterminado si falta
        return True

# Configuración de logging sin el parámetro `encoding`
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - [ID: %(transaction_id)s] - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
            # Quitar el parámetro "encoding" aquí
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Función para configurar el logging
def setup_logging():
    logging.config.dictConfig(LOGGING)  # Configura el logging

    # Obtener el logger raíz
    logger = logging.getLogger()
    logger.addFilter(TransactionIDFilter())

    # Configurar el encoding a utf-8 en el StreamHandler manualmente
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setStream(sys.stdout)  # Asegurarse de que el stream es sys.stdout
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - [ID: %(transaction_id)s] - %(message)s"))
