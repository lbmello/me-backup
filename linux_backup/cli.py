
import click


class cli:
    def __init__(self, tasks):
        self.tasks = tasks

        @click.group()
        def main_cli():
            ...

        @click.command(name = 'run_now', help = 'Run the backup tasks right now.')
        def now():
            for task in self.tasks:
                task.run_now()


        @click.command(name = 'shedule', help = 'Schedule the tasks to run using your time configurations.')
        def schedule():
            for task in self.tasks:
                task.schedule()


        @click.command(name = 'print_rsync', help = 'Return the rsync command')
        def rsync():
            for task in self.tasks:
                task.show_rsync_script()


        main_cli.add_command(now)
        main_cli.add_command(schedule)
        main_cli.add_command(rsync)
        
        main_cli()
