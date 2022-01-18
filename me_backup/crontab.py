
from crontab import CronTab


class cron:

    def __init__(self, commands, frequency, path='/etc/crontab', user='root'):
        self.commands = commands
        self.frequency = frequency
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
            
            if (cron_reference in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(self.commands)

            elif (cron_reference not in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(f"{cron_reference}{self.commands}")

        # Write the reference and the commands to file in /var/spool/cron/[default_user]
        elif self.path == f"/var/spool/cron/{self.user}":
            cron_file = open(self.path, 'r+')
            cron_lines = cron_file.readlines()
            
            if (self.commands not in cron_lines):
                cron_file.write(self.commands)
        
        # Create custom file in default_crontab_path location 
        else:
            custom_crontab = open(self.path, 'w')
            custom_crontab.write(self.commands)

            # Write the reference and input the source to file in /etc/crontab
            cron_file = open('/etc/crontab', 'r+')
            cron_lines = cron_file.readlines()

            if (cron_reference in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(self.commands)

            elif (cron_reference not in cron_lines) and (self.commands not in cron_lines):
                cron_file.write(f"{cron_reference}{source}")

        cron_file.close()


    def clear_crontab(self):
        """Remove all the content of the crontab file."""
        
        cron_file = open(self.path, 'w')
        cron_file.close()


    def create_crontab(self):
        """Create a CronTab object, process the string of time and configure crontab."""

        self._cron = CronTab(
            user = self.user,
            tabfile = self.path
        )
        self.job = self._cron.new(command=self.commands)
        
        if 'shortcut' in self.frequency:
            shortcut = self.frequency['shortcut']

            if shortcut == 'hourly':
                self.job.hour.every(1)
            
            elif shortcut == 'daily':
                self.job.hour.every(24)

            elif 'weekly' in shortcut:
                if shortcut == 'weekly':
                    self.job.day.every(7)
                elif shortcut == 'weekly_sunday':
                    self.job.dow.on('SUN')
                elif shortcut == 'weekly_monday':
                    self.job.dow.on('MON')
                elif shortcut == 'weekly_tuesday':
                    self.job.dow.on('TUE')
                elif shortcut == 'weekly_wednesday':
                    self.job.dow.on('WED')       
                elif shortcut == 'weekly_thursday':
                    self.job.dow.on('THU')
                elif shortcut == 'weekly_friday':
                    self.job.dow.on('FRI')     
                elif shortcut == 'weekly_saturday':
                    self.job.dow.on('SAT')

            elif 'monthly' in shortcut:
                if shortcut == 'monthly':
                    self.job.day.every(30)
                elif shortcut == 'monthly_january':
                    self.job.month.on('JAN')
                elif shortcut == 'monthly_februay':
                    self.job.month.on('FEB')
                elif shortcut == 'monthly_march':
                    self.job.month.on('MAR')
                elif shortcut == 'monthly_april':
                    self.job.month.on('APR')
                elif shortcut == 'monthly_may':
                    self.job.month.on('MAY')
                elif shortcut == 'monthly_june':
                    self.job.month.on('JUN')
                elif shortcut == 'monthly_july':
                    self.job.month.on('JUL')
                elif shortcut == 'monthly_august':
                    self.job.month.on('AUG')
                elif shortcut == 'monthly_september':
                    self.job.month.on('SEP')
                elif shortcut == 'monthly_october':
                    self.job.month.on('OCT')
                elif shortcut == 'monthly_november':
                    self.job.month.on('NOV')
                elif shortcut == 'monthly_december':
                    self.job.month.on('DEC')

        elif 'cron_syntax' in self.frequency:
            ...
            # TODO: Implantar opcao para input do padrao do cron no yaml direto pro crontab
        
        self._cron.write()

