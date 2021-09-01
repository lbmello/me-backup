
import logging
import subprocess


from .backup import backup as _backup
from .crontab import cron as _cron
from .wake_on_lan import wake_on_lan as _wol


class task:

    def __init__(self, task, global_config):
        self.name = task['name']
        self.slug = task['slug']
        self.src = task['src']
        self.dst = task['dst']
        self.frequency = task['frequency']

        # Global check - Verify if host, user and frequency are informed in global or task section
        if 'host' in task:
            self.host = task['host']
        elif 'default_host' in global_config:
            self.host = global_config['default_host']
        else:
            logging.debug(f'Host of task {self.name} and global host not informed.')
 
        if 'user' in task:
            self.user = task['user']
        elif 'default_user' in global_config:
            self.user = global_config['default_user']
        else:
            logging.debug(f"User of task {self.name} and global user not informed.")

        if 'frequency' in task:
            self.frequency = task['frequency']
        elif 'default_frequency' in global_config:
            self.frequency = global_config['default_frequency']
        else:
            logging.debug(f"Frequency of task {self.name} and global frequency not informed.")
        
        # Task checks - Verify if exclude was informed
        if 'exclude' in task:
            self.exclude = task['exclude']
        else:
            self.exclude = None
            logging.debug(f"Exclude field not informed in {self.name} task.")

        # Wake on Lan - If true, send magic packet to MAC
        if 'wake_on_lan' in task:
            self.wol_enabled = task['wake_on_lan']['enabled']
            self.wol_mac_address = task['wake_on_lan']['mac_address']
            self.wol_run()
               
 
        # Create rsync commands
        self._process_rsync_commands()

        # TODO: Implantar tratamento de usuario e path do crontab nao informado
        self.cron = _cron(
            commands = self.rsync,
            frequency = self.frequency,
            path = global_config['crontab_path'],
            user = self.user
        )
                

    def schedule(self):
        """Schedule the rsync over cron."""

        self.cron.create_crontab()


    def run_now(self):
        """Run command right now with subprocess and print the stdout."""

        out = subprocess.getoutput(self.rsync)

        print('saida', out)
        print('comando', self.rsync)
        print('___________________')


    def show_rsync_script(self):
        """Show the exact rsync command, not run os schedule."""

        print(self.rsync)


    def wol_run(self):
        """Instance wake_on_lan and run method to send meagic packet."""

        if self.wol_enabled:
            wol = _wol(
                mac_address = self.wol_mac_address 
            )

            wol.send_package()


    def _process_rsync_commands(self):
        """Instance backup object and get the return of create_rsync function."""
        
        bkp = _backup(
            source = self.src,
            destination = self.dst, 
            exclude = self.exclude
        )

        if self.host and self.user:
            self.rsync = bkp.create_remote_rsync(
                host = self.host, 
                user = self.user,
            )
        else:
            self.rsync = bkp.create_rsync()
