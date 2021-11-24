
from os import chmod, path
import stat
import logging
from shutil import chown


class install:

    def __init__(self, config, config_obj):
        self.config_obj = config_obj
        self.config = config

        self.default_user = self.config['default_user']
        self.default_group = self.config['default_user']
        self.permission = stat.S_IRWXU + stat.S_IRWXG
        self.files = [
            f"/var/spool/cron/{self.default_user}",
            f"{self.config['task_file']}",
            f"{self.config['log_path']}",
        ]

  
    def validate_installation(self):
        """Check if the instaled parameter is true in config file."""

        if 'instaled' in self.config:
            if (self.config['instaled'] == 'False') or (self.config['instaled'] == 'false'):
                self.instaled = False
            else:
                self.instaled = True
        else:
            logging.debug('instaled parameter not present at config file.')

        return self.instaled


    def close_file(self):
        """Close cofnig file."""

        self.config_obj.close_file()


    def set_instaled_true(self):
        """Set instaled as true in config file."""

        self.config_obj.set_instaled_true()


    def create_crontab_files(self):
        """Create crontab file to default_user in config file."""

        for file in self.files:
            # If not exist, create a blank File
            if not path.exists(file):
                try:
                    with open(file, 'w') as f:
                        f.write("")
                        f.close()
                    logging.info(f'File {file} created with no data.')
                
                except FileNotFoundError:
                    logging.error(f"File {file} not found.")

                except:
                    logging.error(f"Generic error while creating file {file}.")
                    
            # Change file permission
            try:
                chmod(file, self.permission)
                logging.info(f"Applied 644 permission to {file}.")
            except:
                logging.error(f"Generic error while change permission of file {file}.")

            # Change owner to defaul user
            try:
                chown(
                    file, 
                    user = self.default_user,
                    group = self.default_group
                )
                logging.info(f"Applied {self.default_user}:{self.default_group} owners to file {file}.")
            except:
                logging.error(f"Generic error while change owner of file {file}.")

            
    def fill_default_task_file(self):
        """Fill the default task_file with task_example.yaml data."""

        module_path = path.abspath(path.dirname(__file__))

        example_task_lines = open((path.join(module_path, "task_example.yaml")),'r').readlines()
        default_task_lines = open(f"{self.config['task_file']}", 'r').readlines()
        if not default_task_lines:
            with open(f"{self.config['task_file']}", 'a') as f:
                f.writelines(example_task_lines)
                logging.info(f"{self.config['task_file']} filled with task_example.yaml data.")
        else:
            logging.info(f"{self.config['task_file']} already created, not needed to fill data with task_example.yaml.")
            

    def install_dependencies(self):
        ...