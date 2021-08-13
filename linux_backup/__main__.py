
from os.path import isfile


from .data import data as _data
from .task import task as _task


if __name__ == "__main__":
    d = _data(
        task_file = "/home/lucas/Documents/GitHub/linux-backup/tasks.yaml"
    )

    # Clear crontab file
    try:
        crontab_file = open(d.global_config['crontab_path'], 'w')
        crontab_file.close()
    except KeyError:
        pass

    tasks = list()

    for t in d.tasks:
        task_obj = (
            _task(
                task = t,
                global_config = d.global_config
            )
        )

        #task_obj.run_now()

        tasks.append(task_obj)
