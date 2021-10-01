
import os


def is_config_exist(config_path):
    
    if os.path.exists(config_path):
        return True
    else:
        return False


def create_config_file(config_path):

    print('Me-backup never runned, this follow steps will create the tool folder and config file into /etc/me-backup! (need sudo)')

    user = input("Default User: [root] ") or 'root',
    task_file = input("Task file: [/etc/me-backup/tasks.yaml] ") or '/etc/me-backup/tasks.yaml'
    log_path = input("Log path: [/etc/me-backup/mebk.log] ") or '/etc/me-backup/mebk.log'
    log_level = input("Log level: [INFO] ") or 'INFO'
    default_host = input("Default host: [127.0.0.1] ") or '127.0.0.1'
    default_crontab_path = input(f"Default crontab path: [/var/spool/{user[0]}] ") or f"/var/spool/{user[0]}"

    lines = [
        f"default_user = {user[0]}\n", 
        f"task_file = {task_file}\n", 
        f"log_path = {log_path}\n",
        f"log_level = {log_level}\n",
        f"default_host = {default_host}\n",
        f"default_crontab_path = {default_crontab_path}\n"]
    
    if is_config_exist(config_path):
        with open(config_path, 'w') as config:
            config.writelines(lines)
    else:
        os.mkdir(os.path.dirname(config_path))

        with open(config_path, 'w') as config:
            config.writelines(lines)
    

def process_config_lines(config_file):
    """Method used to process config file columns."""

    config_lines = config_file.readlines()

    config_values = dict()

    for line in config_lines:
        line = line.replace('\n', '')

        key, value = line.split(' = ')

        config_values[key] = value

    return config_values