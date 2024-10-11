
import logging

from airless.core.utils import get_config


class BaseClass():

    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')
        logging.basicConfig(level=logging.getLevelName(get_config('LOG_LEVEL')))
        self.logger.debug(f'Created class instance {self.__class__.__name__}')
