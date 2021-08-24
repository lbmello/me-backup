
import click


class cli:
    def __init__(self, tasks):
        self.tasks = tasks

        @click.group()
        def main_cli():
            ...

        @click.command(help = 'Run the backup tasks right now.')
        def now(name = 'run_now'):
            for task in self.tasks:
                task.run_now()


        @click.command(help = 'Schedule the tasks to run using your time configurations.')
        def schedule(name = 'shedule'):
            for task in self.tasks:
                task.schedule()


        main_cli.add_command(now)
        main_cli.add_command(schedule)
        
        main_cli()
