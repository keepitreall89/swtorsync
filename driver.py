import os
import pathlib

class SettingsLocatory:
    def __init__(self):
        self.localAppDataPath = pathlib.Path(os.getenv('LOCALAPPDATA'))
        self.swtorDirectory = self.localAppDataPath+"/SWTOR/swtor/settings/"