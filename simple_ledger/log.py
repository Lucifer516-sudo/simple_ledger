from simple_ledger._log import Logger

logger = Logger()
logger.add_more_loggers(logger_names=["kivy"])
