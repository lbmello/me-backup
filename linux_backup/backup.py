
import logging
import os
import yaml

class backup:

    def __init__(self, source, destination, exclude):
        self.source = source
        self.destination = destination
        self.exclude = exclude


    def create_remote_rsync(self, host, user):
        """Create rsync full command with ssh connection."""

        self.host = host
        self.user = user

        cmd = f"rsync -av --exclude={self._create_exclude_pattern()} {self.source} {self.user}@{self.host}:{self.destination}"
        
        return cmd


    def create_rsync(self):
        """Create rsync full command with local src and dst."""

        cmd = f"""rsync -av --exclude={self._create_exclude_pattern()} {self.source} {self.destination}"""
        print('comando', cmd)
        
        return cmd


    def _create_exclude_pattern(self):
        """Create the patterns to exclude command."""

        # TODO: Ajustar para patterns validos

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
