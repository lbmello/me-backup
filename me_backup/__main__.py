
import os
import logging


from .cli import cli as _cli
from .config import config as _config
from .data import data as _data
from .definitions import ROOT_DIR, CONFIG_PATH
from .log import log as _log
from .task import task as _task
from .utils import process_config_lines, is_config_exist, create_config_file



if __name__ == "__main__":
    """
    if is_config_exist(CONFIG_PATH):
        conf_file = open(CONFIG_PATH, 'r')
    else:
        create_config_file(CONFIG_PATH)
        conf_file = open(CONFIG_PATH, 'r')
    """

    c = _config(CONFIG_PATH)
    
    config = c.process_config_lines()

    d = _data(
        task_file = config['task_file']
    )

    # Clear project crontab file, if them exist
    if 'default_crontab_path' in config:
        if config['default_crontab_path'] != ('/etc/crontab' or 'user'):
            try:
                crontab_file = open(config['default_crontab_path'], 'w')
                crontab_file.close()
            except KeyError:
                logging.error(f"error while reading project crontab file in {config['default_crontab_path']}.")

    # logging configs
    l = _log(
        path = config['log_path'],
        level = config['log_level']
    )

    # instance of tasks and CLI
    tasks = list()

    for task in d.tasks:
        task_obj = (
            _task(
                task = task,
                global_config = config
            )
        )

        tasks.append(task_obj)

    c = _cli(
        config = c,
        tasks = tasks
    )

