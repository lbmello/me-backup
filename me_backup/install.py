
from os import chmod, path
import stat
import logging
from shutil import chown



class install:

    def __init__(self, config, config_obj):
        self.config_obj = config_obj
        self.config = config

  
    def validate_installation(self):
        """Check if the instaled parameter is true in config file."""

        if 'instaled' in self.config:
            if self.config['instaled'] == ('True' or 'true'):
                self.instaled = True
            else:
                self.instaled = False
        else:
            logging.debug('instaled parameter not present at config file.')

        return self.instaled


    def close_file(self):
        self.config_obj.close_file()

    def set_instaled_true(self):
        self.config_obj.set_instaled_true()


    def create_crontab_files(self):
        """Create crontab file to default_user in config file."""

        default_user = self.config['default_user']
        default_group = self.config['default_user']
        permission = stat.S_IRWXU + stat.S_IRWXG

        files = [
            f"/var/spool/cron/{default_user}"
        ]

        for file in files:
            try:
                # Create File
                with open(file, 'w') as f:
                    f.write("")
                    f.close()
                
                # Change file permission
                chmod(file, permission)

                # Change owner to defaul user
                chown(
                    file, 
                    user=default_user,
                    group=default_group
                )
                
                # TODO: Botar permissao no log - XXX
                logging.info(f'File {file} created with XXX permission to {default_user}:{default_group}.')
            
            except FileNotFoundError:
                logging.error(f"File {file} not found.")


    def install_dependencies(self):
        ...