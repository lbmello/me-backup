
import logging


class log:

    def __init__(self, path, level):
        self.log_path = path
        self.level = level


        logging.basicConfig(
            filename = self.log_path, 
            level = self.level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )

        logging.info(msg = f'me-backup started.')
