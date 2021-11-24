
import click
import logging
import os

from .install import install as _install


class cli:
    def __init__(self, tasks, config):
        self.tasks = tasks
        self.config_obj = config
        self.config = self.config_obj.process_config_lines()
        self.instaled = self.config['instaled']

        @click.group()
        def main_cli():
            ...

        @click.command(name = 'run_now', help = 'Run the backup tasks right now.')
        def now():
            for task in self.tasks:
                task.run_now()


        @click.command(name = 'schedule', help = 'Schedule the tasks to run using your time configurations.')
        def schedule():
            for task in self.tasks:
                task.schedule()


        @click.command(name = 'print_rsync', help = 'Return the rsync command')
        def rsync():
            for task in self.tasks:
                task.show_rsync_script()


        @click.command(name = 'generate_yaml', help = 'Create a tasks.yaml model file.')
        @click.argument('crontab_file', type=click.File('wb'))
        def generate_yaml(crontab_file):
            with open('task_example.yaml', 'r') as input:
                for line in input:
                    crontab_file.write(
                        bytes(line, encoding='utf-8')
                    )


        @click.command(name = 'install', help = 'Create needed files (run with sudo).')
        def install():
            i = _install(
                config=self.config,
                config_obj=self.config_obj
            )

            self.instaled = i.validate_installation()

            if not self.instaled:
                i.create_crontab_files()
                i.set_instaled_true()
                i.fill_default_task_file()
            

        # TODO: Ajust this part to read a boolean, not string
        if self.instaled == 'false' or self.instaled == 'False':
            main_cli.add_command(install)
        else:
            main_cli.add_command(now)
            main_cli.add_command(schedule)
            main_cli.add_command(rsync)
            main_cli.add_command(generate_yaml)
        
                
        
        main_cli()
