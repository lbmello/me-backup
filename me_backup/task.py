
import logging
import subprocess


from .backup import backup as _backup
from .crontab import cron as _cron
from .wake_on_lan import wake_on_lan as _wol


class task:

    def __init__(self, task, global_config):
        self.name = task['name']
        self.slug = task['slug']
        self.frequency = task['frequency']

        # Check if its a local or remote task to set source and destination
        if 'src' in task:
            self.src = task['src']
        elif 'src_path' in task:
            self.src = task['src_path']
        
        if 'dst' in task:
            self.dst = task['dst']
        elif 'dst_path' in task:
            self.dst = task['dst_path']

        # Remote source check with their dependencies
        if 'remote_src' in task:
            self.remote_src = task['remote_src']
            if self.remote_src:
                
                if 'src_path' in task:
                    self.src = task['src_path']
                else:
                    logging.error(f"src_path not informed in task {self.name}")

                if 'src_host' in task:
                    self.src_host = task['src_host']
                else:
                    self.src_host = None
                    logging.error(f"src_host not informed in task {self.name}")
            else:
                self.src_host = None

        else:
            self.remote_src = False

        # Remote destination check with their dependencies
        if 'remote_dst' in task:
            self.remote_dst = task['remote_dst']
            if self.remote_dst:
                
                if 'dst_path' in task:
                    self.dst = task['dst_path']
                else:
                    logging.error(f"dst_path not informed in task {self.name}")

                if 'dst_host' in task:
                    self.dst_host = task['dst_host']
                else:
                    self.dst_host = None
                    logging.error(f"dst_host not informed in task {self.name}")
            else:
                self.dst_host = None
        else:
            self.remote_dst = False

        # TODO: VALIDAR SE PRECISO DESSE PARAMETRO HOST
        """
        # Global check - Verify if host, user and frequency are informed in global or task section
        if 'host' in task:
            self.host = task['host']
        elif 'default_host' in global_config:
            self.host = global_config['default_host']
        else:
            logging.debug(f'Host of task {self.name} and global host not informed.')
        """
 

        if 'user' in task:
            self.user = task['user']
        elif 'default_user' in global_config:
            self.user = global_config['default_user']
        else:
            logging.debug(f"User of task {self.name} and global user not informed.")


        if 'default_crontab_path' in global_config:
            if global_config['default_crontab_path'] == 'user':
                self.crontab_path = f"/var/spool/cron/{self.user}"
                logging.debug(f"Crontab file configured in {self.crontab_path}")
            
            elif global_config['default_crontab_path'] == 'crontab':
                self.crontab_path = f"/etc/crontab"
                logging.debug(f"Crontab file configured in {self.crontab_path}")
            
            else:
                self.crontab_path = global_config['default_crontab_path']
                logging.debug(f"Crontab file configured in {self.crontab_path}")
        else:
            self.crontab_path = '/etc/crontab'
            logging.debug(f"Crontab file configured by default in {self.crontab_path}")


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
            self.wol_ip = task['wake_on_lan']['ip']
            self._wol_run()


        # Type of execution select, sync of version the files at destination
        # TODO: terminar implantação dessa parte, considerando como executar o sync completo e o versionado, com historico de versao

        if 'copy_config' in task:
            if task['copy_config']['type'] == 'sync':
                self.copy_config = {
                    'copy_type': task['copy_config']['type']
                }
            elif task['copy_config']['type'] == 'version':
                self.copy_config = {
                    'copy_type': task['copy_config']['type'],
                    'versions_qtd': task['copy_config']['versions_qtd'],
                    'tmp_folder': task['copy_config']['tmp_folder']
                }
            else:
                self.copy_config = {
                    'copy_type': 'sync'
                }
      
 
        # Create rsync commands
        self._process_rsync_commands()

        self.cron = _cron(
            commands = self.rsync,
            frequency = self.frequency,
            task_name = self.name,
            path = self.crontab_path,
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


    def _wol_run(self):
        """Instance wake_on_lan and run method to send meagic packet."""

        if self.wol_enabled:
            wol = _wol(
                mac_address = self.wol_mac_address,
                ip = self.wol_ip 
            )


    def _process_rsync_commands(self):
        """Instance backup object and get the return of create_rsync function."""
        
        bkp = _backup(
            exclude = self.exclude,
        )

        # If remote src and dst are False, create rsync commands locally
        if not self.remote_src and not self.remote_dst:
            self.rsync = bkp.create_rsync(
                source = self.src,
                destination = self.dst, 
            )
        
        # If , create remote rsync
        elif (self.src and self.dst and self.user):
            self.rsync = bkp.create_remote_rsync(
                remote_src = self.remote_src, 
                source = self.src,
                src_host = self.src_host, 
                remote_dst = self.remote_dst, 
                destination = self.dst, 
                dst_host = self.dst_host, 
                user = self.user
            )
            
        else:
            logging.error(f"error to process rsync logic in the task {self.name}.")