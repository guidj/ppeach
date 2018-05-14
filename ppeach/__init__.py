import logging

logger = logging.getLogger('ppeach')
logger.setLevel(logging.DEBUG)

__formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')

__sh = logging.StreamHandler()
__sh.setFormatter(__formatter)
logger.addHandler(__sh)
