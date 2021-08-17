
import logging
import subprocess


from .backup import backup as _backup
from .crontab import cron as _cron

class task:

    def __init__(self, task, global_config):
        self.name = task['name']
        self.slug = task['slug']
        self.src = task['src']
        self.dst = task['dst']
        self.exclude = task['exclude']
        self.frequency = task['frequency']

        # Verify if host, user and frequency are informed in global and task section
        if 'host' in task:
            self.host = task['host']
        elif 'host' in global_config:
            self.host = global_config['host']
        else:
            logging.debug(f'Host of task {self.name} and global host not informed.')
 
        if 'user' in task:
            self.user = task['user']
        elif 'user' in global_config:
            self.user = global_config['user']
        else:
            logging.debug(f'User of task {self.name} and global user not informed.')

        if 'frequency' in task:
            self.frequency = task['frequency']
        elif 'frequency' in global_config:
            self.frequency = global_config['frequency']
        else:
            logging.debug(f'Frequency of task {self.name} and global frequency not informed.')
        

        # Create rsync commands
        self._process_rsync_commands()

        self.cron = _cron(
            commands = self.rsync,
            frequency = self.frequency,
            path = global_config['crontab_path'],
            user = global_config['user']
        )
                
        self.schedule()


    def schedule(self):
        """."""

        self.cron.create_crontab()


    def run_now(self):
        """Run command right now."""

        print('comando -> ', self.rsync)

        out = subprocess.getoutput(self.rsync)

        print(out)
        print('___________________')


    def _process_rsync_commands(self):
        """Instance backup object and get the return of create_rsync function."""
        
        bkp = _backup(
            source = self.src,
            destination = self.dst, 
            exclude = self.exclude
        )

        if self.host and self.user:
            bkp.create_remote_rsync(
                host = self.host, 
                user = self.user,
            )
        else:
            bkp.create_rsync()

        self.rsync = bkp.create_rsync()
