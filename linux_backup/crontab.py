
from crontab import CronTab


class cron:

    def __init__(self, commands, frequency, path='/etc/crontab', user='root'):
        self.commands = commands
        self.frequency = frequency
        self.path = path
        self.user = user

        self._attach_crontab()


    def _attach_crontab(self):
        """Add the source to project's crontab file into /etc/crontab."""

        cron_reference = "# me-backup source\n"
        source = f"source {self.path}\n"
        
        cron_file = open('/etc/crontab', 'r+')
        cron_lines = cron_file.readlines()
        
        if self.path == '/etc/crontab':
            for line in cron_lines:
                print('linha', line)
                if (cron_reference in line) and (self.commands not in cron_lines):
                    cron_file.write(self.commands)
        else:
            for line in cron_lines:
                if (cron_reference in line) and (source not in cron_lines):
                    cron_file.write(source)

        cron_file.close()


    def clear_crontab(self):
        """Remove all the content of the crontab file."""
        
        cron_file = open(self.path, 'w')
        cron_file.close()


    def create_crontab(self):
        """TODO: Deve ler as tarefas com os tempos e adicionar parametros no crontab."""

        self._cron = CronTab(
            user='lucas',
            tabfile=self.path
        )
        self.job = self._cron.new(command=self.commands)
        self.job.minute.every(1)

        self._cron.write()

