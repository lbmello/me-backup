
from crontab import CronTab
import logging


class cron:

    def __init__(self, commands, frequency, task_name, path='/etc/crontab', user='root'):
        self.commands = commands
        self.frequency = frequency
        self.task_name = task_name
        self.path = path
        self.user = user

        self._attach_crontab()


    def _attach_crontab(self):
        """Add the runnable part in the crontab file configured."""

        cron_reference = "# me-backup commands\n"
        source = f"source {self.path}\n"
        
        # Write the reference and the commands to file in /etc/crontab
        if self.path == '/etc/crontab':
            cron_file = open(self.path, 'r+')
            cron_lines = cron_file.readlines()
            logging.debug(f"file /etc/crontab loaded.")
            
            if (cron_reference in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(self.commands)
                logging.debug(f"cron command || {self.commands} || added in {self.path}.")

            elif (cron_reference not in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(f"{cron_reference}{self.commands}")
                logging.debug(f"cron reference and command || {self.commands} || added in {self.path}.")

        # Write the reference and the commands to file in /var/spool/cron/[default_user]
        elif self.path == f"/var/spool/cron/{self.user}":
            cron_file = open(self.path, 'r+')
            cron_lines = cron_file.readlines()
            logging.debug(f"file {self.path} loaded.")
            
            if (self.commands not in cron_lines):
                cron_file.write(self.commands)
                logging.debug(f"cron command || {self.commands} || added in {self.path}.")
        
        # Create custom file in default_crontab_path location 
        else:
            custom_crontab = open(self.path, 'w')
            custom_crontab.write(self.commands)
            logging.debug(f"Custom cronfile selected to file {self.path}.")

            # Write the reference and input the source to file in /etc/crontab
            cron_file = open('/etc/crontab', 'r+')
            cron_lines = cron_file.readlines()
            logging.debug('/etc/crontab opened to input source.')

            if (cron_reference in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(self.commands)
                logging.debug(f"cron command || {self.commands} || added in {self.path}.")

            elif (cron_reference not in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(f"{cron_reference}{source}")
                logging.debug(f"cron reference and command || {self.commands} || added in {self.path}.")

        cron_file.close()


    def clear_crontab(self):
        """Remove all the content of the crontab file."""
        
        cron_file = open(self.path, 'w')
        cron_file.close()
        logging.debug(f"crontab file {self.path} cleaned.")


    def create_crontab(self):
        """Create a CronTab object, process the string of time and configure crontab."""

        self._cron = CronTab(
            user = self.user,
            tabfile = self.path
        )
        self.job = self._cron.new(command=self.commands)
        logging.debug(f"crontab object created with the command {self.commands}")
        
        if 'shortcut' in self.frequency:
            shortcut = self.frequency['shortcut']

            if shortcut == 'hourly':
                self.job.hour.every(1)
                logging.debug(f"time hourly applied to the task {task_name}.")
            
            elif shortcut == 'daily':
                self.job.hour.every(24)
                logging.debug(f"time daily applied to the task {task_name}.")

            elif 'weekly' in shortcut:
                if shortcut == 'weekly':
                    self.job.day.every(7)
                    logging.debug(f"time weekly applied to the task {task_name}.")
                
                elif shortcut == 'weekly_sunday':
                    self.job.dow.on('SUN')
                    logging.debug(f"time weekly_sunday applied to the task {task_name}.")

                elif shortcut == 'weekly_monday':
                    self.job.dow.on('MON')
                    logging.debug(f"time weekly_monday applied to the task {task_name}.")
                
                elif shortcut == 'weekly_tuesday':
                    self.job.dow.on('TUE')
                    logging.debug(f"time weekly_tuesday applied to the task {task_name}.")
                
                elif shortcut == 'weekly_wednesday':
                    self.job.dow.on('WED')       
                    logging.debug(f"time weekly_wednesday applied to the task {task_name}.")
                
                elif shortcut == 'weekly_thursday':
                    self.job.dow.on('THU')
                    logging.debug(f"time weekly_thursday applied to the task {task_name}.")
                
                elif shortcut == 'weekly_friday':
                    self.job.dow.on('FRI')     
                    logging.debug(f"time weekly_friday applied to the task {task_name}.")
                
                elif shortcut == 'weekly_saturday':
                    self.job.dow.on('SAT')
                    logging.debug(f"time weekly_saturday applied to the task {task_name}.")

            elif 'monthly' in shortcut:
                if shortcut == 'monthly':
                    self.job.day.every(30)
                    logging.debug(f"time montly applied to the task {task_name}.")
                elif shortcut == 'monthly_january':
                    self.job.month.on('JAN')
                    logging.debug(f"time JAN applied to the task {task_name}.")

                elif shortcut == 'monthly_februay':
                    self.job.month.on('FEB')
                    logging.debug(f"time FEB applied to the task {task_name}.")

                elif shortcut == 'monthly_march':
                    self.job.month.on('MAR')
                    logging.debug(f"time MAR applied to the task {task_name}.")

                elif shortcut == 'monthly_april':
                    self.job.month.on('APR')
                    logging.debug(f"time APR applied to the task {task_name}.")

                elif shortcut == 'monthly_may':
                    self.job.month.on('MAY')
                    logging.debug(f"time MAY applied to the task {task_name}.")

                elif shortcut == 'monthly_june':
                    self.job.month.on('JUN')
                    logging.debug(f"time JUN applied to the task {task_name}.")

                elif shortcut == 'monthly_july':
                    self.job.month.on('JUL')
                    logging.debug(f"time JUL applied to the task {task_name}.")

                elif shortcut == 'monthly_august':
                    self.job.month.on('AUG')
                    logging.debug(f"time AUG applied to the task {task_name}.")

                elif shortcut == 'monthly_september':
                    self.job.month.on('SEP')
                    logging.debug(f"time SEP applied to the task {task_name}.")

                elif shortcut == 'monthly_october':
                    self.job.month.on('OCT')
                    logging.debug(f"time OCT applied to the task {task_name}.")

                elif shortcut == 'monthly_november':
                    self.job.month.on('NOV')
                    logging.debug(f"time NOV applied to the task {task_name}.")

                elif shortcut == 'monthly_december':
                    self.job.month.on('DEC')
                    logging.debug(f"time DEC applied to the task {task_name}.")


        elif 'cron_syntax' in self.frequency:
            ...
            # TODO: Implantar opcao para input do padrao do cron no yaml direto pro crontab
        
        self._cron.write()

