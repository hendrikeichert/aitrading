import logging

# define the logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

class AiTrader:

    def __init__(self):
        self.alpaca = None

    def initialize(self):        
        logger.info('initialize')
        creds = collect_creds()
        self.alpaca = Alpaca(api_key=creds["API_KEY"], api_secret=creds["API_SECRET"])

