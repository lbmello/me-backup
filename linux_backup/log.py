
import logging
from datetime import datetime


class log:

    def __init__(self, path, level):
        self.log_path = path
        self.level = level
        self.date = datetime.now()

        logging.basicConfig(
            filename = self.log_path, 
            level = self.level
        )

        logging.info(msg = f'me-backup started at {self.date}.')
