
from .cli import cli as _cli
from .data import data as _data
from .log import log as _log
from .task import task as _task


if __name__ == "__main__":
    d = _data(
        task_file = "/home/lucas/Documents/GitHub/linux-backup/tasks.yaml"
    )

    # Clear crontab file
    if d.global_config['crontab_path'] != '/etc/crontab':
        try:
            crontab_file = open(d.global_config['crontab_path'], 'w')
            crontab_file.close()
        except KeyError:
            pass

    # logging configs
    l = _log(
        path = d.global_config['log_path'],
        level = d.global_config['log_level']
    )


    # instance of tasks and CLI
    tasks = list()

    for task in d.tasks:
        task_obj = (
            _task(
                task = task,
                global_config = d.global_config
            )
        )

        tasks.append(task_obj)

    c = _cli(tasks = tasks)
