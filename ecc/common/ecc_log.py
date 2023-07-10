import logging

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename='ecc.log', level=logging.INFO, format=log_format, filemode='w')
ecc_logger = logging.getLogger()

