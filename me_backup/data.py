
import logging
import os
import yaml


class data:

    def __init__(self, task_file):
        self.task_file = task_file

        self.tasks = dict()

        if self.is_config_exist:
            try:
                _raw_object = open(self.task_file, 'r')

                self.yaml_file = yaml.load(_raw_object, Loader = yaml.FullLoader)
                
                _raw_object.close()

                self.tasks = self.yaml_file['tasks']

            except:
                logging.critical(f"Fail to read {self.task_file} file!")

        else:
            logging.critical(f"File {self.task_file} not exist.")



    def is_config_exist(self):
        """Return true if config.yaml exists."""
        
        return os.path.isfile(self.task_file)


    def process_file(self):
        """TODO: deve ler cada chave do arquivo e gerar uma variavel especifica"""
        ...