import logging
from datetime import datetime

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", datetime.utcnow().strftime('%Y-%m-%d')))
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

logger.setLevel(logging.INFO)
