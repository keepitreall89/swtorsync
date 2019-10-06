import os
import pathlib
import configparser


'''Object to store category and decription of setting keys in an organized way.'''
class Setting:
    def __init__(self, category, description):
        self.category = category
        self.description = description
    def __str__(self):
        return str(self.category)+", "+str(self.description)
    def __repr__(self):
        return str(self)

'''Parses or writes a settings file using configparser'''
class Settings:
    setting_mapping = {"ChatColors" : Setting("Chat", "Chat Colors"),
                       "ChatChannels": Setting("Chat", "Chat Channels"),
                       "ChatPanel_1Index": Setting("Chat", "Chat Index"),
                       "GUI_ChatFrameVisible": Setting("Chat", "Chat Frame visibility"),
                       "GUI_Current_Profile": Setting("GUI", "GUI Profile"),
                       "GUI_MiniMapZoom": Setting("GUI", "Minimap Zoom"),
                       "GUI_QuickslotLockState": Setting("GUI", "Quick bar lock state"),
                       "GUI_GalaxyMapViewedForFirstTime": Setting("Tutorial", "First Time Galaxy Map Tutorial"),
                       "GUI_GCConfirmOpenPack": Setting("Confirmation", "Galactic Command Crate confirmation")}
    def __init__(self, file_path):
        self.file_path = pathlib.Path(file_path)
        self.error = False
        self.config = None
        #cast to path, parse version number
        try:
            self.config = configparser.ConfigParser(delimiters="=")
            self.config.read_file(file_path)
            if not ("ChatChannels" in self.config['Settings'].keys() and "GUI_Current_Profile" in self.config['Settings'].keys()):
                self.error = True
        except:
            self.error = True
    def write(self):
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)
    def __str__(self):
        return str(self.file_path)
    def __repr__(self):
        return str(self.file_path)+'\n'+str(self.config)
        



class SettingsLocater:
    def __init__(self, directory=os.getenv('LOCALAPPDATA')):
        self.local_AppData_path = directory
        self.swtor_directory = pathlib.Path(self.local_AppData_path+"/SWTOR/swtor/settings/")
        self.files = []
        self.config_files = []
        if self.swtor_directory.exists():
            children = os.listdir(self.swtor_directory)
            for child in children:
                if not os.path.isdir(self.swtor_directory/child):
                    self.files.append(self.swtor_directory/child)
                filename = str(child).split('.')
                if str(filename[len(filename)-1]).lower()==str('ini').lower():
                    print()
                    #self.config_files.append(FileNameToken(self.swtor_directory/child, child))

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