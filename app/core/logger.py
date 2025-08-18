import logging
import os, sys
from dotenv import load_dotenv
from app.core.middleware import get_transaction_id

load_dotenv()

class TransactionIdInjecter(logging.Filter):
    def filter(self, record):
        record.transaction_id = get_transaction_id() or "no-transaction"
        return True

class CustomLogger:
    def  __init__(self,name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.handlers.clear()
        level = os.environ.get('LOG_LEVEL', 'INFO').upper()
        handler = logging.StreamHandler(sys.stdout if os.environ.get('LOG_STREAM_STDOUT', False) else None)
        handler.setLevel(level)
        handler.addFilter(TransactionIdInjecter())
        formatter = logging.Formatter('%(asctime)s - %(transaction_id)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)