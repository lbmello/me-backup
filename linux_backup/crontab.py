
from crontab import CronTab


class cron:

    def __init__(self, commands, frequency, path=None):
        self.commands = commands
        self.frequency = frequency

        if not path:
            self.path = '/etc/crontab'
        else:
            self.path = path

        self._attach_crontab()


    def _attach_crontab(self):
        """TODO: deve adicionar source do crontab dos bks no crontab principal."""
        
        if self.path != '/etc/crontab':
            ...


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

