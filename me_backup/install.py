
from os import chmod, path
import stat
import logging
from shutil import chown



class install:

    def __init__(self):
        self.instaled = None        


    def validate_installation(self, config):
        """Check if the instaled parameter is true in config file."""

        if config['instaled'] == ('True' or 'true'):
            self.instaled = True
        else:
            self.instaled = False

        return self.instaled


    def crete_basic_file(self, filepath):
        """Create projects folder into the custom path."""
        


    def create_crontab_files(self, config):
        """Create crontab file to default_user in config file."""

        # TODO: CORRIGIR PERMISSIONAMENTO
        default_user = config['default_user']
        default_group = 'lucas'
        permission = stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO

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