
import logging
import os
import yaml

class backup:

    def __init__(self, source, destination, exclude, remote_dst, remote_src):
        self.source = source
        self.destination = destination
        self.exclude = exclude
        self.remote_dst = remote_dst
        self.remote_src = remote_src


    def create_remote_rsync(self, host, user):
        """Create rsync full command with ssh connection."""

        self.host = host
        self.user = user

        if not self.remote_src and self.remote_dst:
            if self.exclude != None:
                cmd = f"rsync -av --exclude={self._create_exclude_pattern()} {self.source} {self.user}@{self.host}:{self.destination}"
            else:
                cmd = f"rsync -av {self.source} {self.user}@{self.host}:{self.destination}"

        elif self.remote_src and not self.remote_dst:
            if self.exclude != None:
                cmd = f"rsync -av --exclude={self._create_exclude_pattern()} {self.user}@{self.host}:{self.source} {self.destination}"
            else:
                cmd = f"rsync -av {self.user}@{self.host}:{self.source} {self.destination}"

        elif self.remote_src and self.remote_dst:
            if self.exclude != None:
                cmd = f"rsync -av --exclude={self._create_exclude_pattern()} {self.user}@{self.host}:{self.source} {self.user}@{self.host}:{self.destination}"
            else:
                cmd = f"rsync -av {self.user}@{self.host}:{self.source} {self.user}@{self.host}:{self.destination}"

        return cmd


    def create_rsync(self):
        """Create rsync full command with local src and dst."""

        if self.exclude != None:
            cmd = f"""rsync -av --exclude={self._create_exclude_pattern()} {self.source} {self.destination}"""
        else:
            cmd = f"""rsync -av {self.source} {self.destination}"""
        
        return cmd


    def _create_exclude_pattern(self):
        """Create the patterns to exclude command."""

        exclude_dict = set()

        if len(self.exclude) == 1:
            if 'files' in self.exclude:
                temp_value = f"{self.exclude['files']}"
            
            if 'extensions' in self.exclude:
                temp_value = f"'*.{self.exclude['extensions'][0]}'"

            if 'folder' in self.exclude:
                temp_value = f"{self.exclude['folder']}/"
            else:
                ...

        elif len(self.exclude) > 1:
            if 'files' in self.exclude:
                for r in self.exclude['files']:
                    exclude_dict.add(r)

            if 'extensions' in self.exclude:
                for r in self.exclude['extensions']:
                    exclude_dict.add(f"*.{r}")
            
            if 'folder' in self.exclude:
                for r in self.exclude['folder']:
                    exclude_dict.add(f"{r}/")

            # at end transform dict to string and take off space of comma dict
            temp_value = str(exclude_dict).replace(', ', ',')

        return temp_value
