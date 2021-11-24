
import os


class config:
    def __init__(self, config_path):
        self.config_path = config_path

        if self.is_config_exist():
            self.config_file = open(self.config_path, 'r')
            self.config_lines = self.config_file.readlines()
            self.config_file.close()
        else:
            self.config_file = open(self.config_path, 'w+')
            self.create_config_file()
        
        self.config_values = dict()


    def _write_lines(self):
        config_file = open(self.config_path, 'w')

        new_lines = list()

        for key, value in self.config_values.items():
            new_lines.append(f'{key} = {value}\n')

        config_file.writelines(new_lines)
        config_file.close()


    def close_file(self):
        self.config_file.close()


    def set_instaled_true(self):
        if self.config_values['instaled'] == 'False' or 'false':
            self.config_values['instaled'] = 'True'
            self._write_lines()


    def process_config_lines(self):
        """Method used to process config file columns."""
        for line in self.config_lines:
            line = line.replace('\n', '')

            key, value = line.split(' = ')

            self.config_values[key] = value

        return self.config_values


    def is_config_exist(self):
        """Check if the file exist in default path."""
        
        if os.path.exists(self.config_path):
            return True
        else:
            return False


    def create_config_file(self):
        """Start the form and create the file inside the defaul path."""

        print('Me-backup never runned, this follow steps will create the tool folder and config file into /etc/me-backup! (need sudo)')

        current_user =  os.getlogin()

        user = input(f"Default User: [{current_user}] ") or f"{current_user}",
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
            f"default_crontab_path = {default_crontab_path}\n",
            f"instaled = false\n"]
        
        if self.is_config_exist():
            self.config_file.writelines(lines)
            self.config_lines = lines
        else:
            os.mkdir(os.path.dirname(self.config_path))
            self.config_file.writelines(lines)
