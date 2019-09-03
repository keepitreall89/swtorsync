import os
import pathlib

class FileNameToken:
    def __init__(self, path, name):
        self.file_path = path
        self.file_name = name
    def __str__(self):
        return str(self.file_path)


class SettingsLocater:
    def __init__(self):
        self.local_AppData_rath = os.getenv('LOCALAPPDATA')
        self.swtor_directory = pathlib.Path(self.local_AppData_rath+"/SWTOR/swtor/settings/")
        self.exists = self.swtor_directory.exists()
        self.files = []
        self.config_files = []
        if self.exists:
            children = os.listdir(self.swtor_directory)
            for child in children:
                if not os.path.isdir(self.swtor_directory/child):
                    self.files.append(self.swtor_directory/child)
                filename = str(child).split('.')
                if str(filename[len(filename)-1]).lower()==str('ini').lower():
                    self.config_files.append(FileNameToken(self.swtor_directory/child, child))

    """Searches through the directory and returns a list of files with an extension matching file_type_extension. Is not case sensetive."""
    def search_again(self):
        self.exists = self.swtor_directory.exists()
        self.files = []
        self.config_files = []
        if self.exists:
            children = os.listdir(self.swtor_directory)
            for child in children:
                if not os.path.isdir(self.swtor_directory/child):
                    self.files.append(self.swtor_directory/child)
            for file in self.files:
                filename = str(file).split('.')
                if str(filename[len(filename)-1]).lower()==str('ini').lower():
                    self.config_files.append(file)


if __name__ == "__main__":
    settings = SettingsLocater()
    for f in settings.config_files:
        print(f.file_name)