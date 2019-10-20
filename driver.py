import os
import pathlib
import configparser
#for debugging only
import sys

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
class Swtor_Toon_Data:
    setting_mapping = {"ChatColors" : Setting("Chat", "Chat Colors"),
                       "ChatChannels": Setting("Chat", "Chat Channels"),
                       "ChatPanel_1Index": Setting("Chat", "Chat Index"),
                       "GUI_ChatFrameVisible": Setting("Chat", "Chat Frame visibility"),
                       "GUI_Current_Profile": Setting("GUI", "GUI Profile"),
                       "GUI_MiniMapZoom": Setting("GUI", "Minimap Zoom"),
                       "GUI_QuickslotLockState": Setting("GUI", "Quick bar lock state"),
                       "GUI_GalaxyMapViewedForFirstTime": Setting("Tutorial", "First Time Galaxy Map Tutorial"),
                       "GUI_GCConfirmOpenPack": Setting("Confirmation", "Galactic Command Crate confirmation"),
                       "Show_Chat_TimeStamp": Setting("Chat", "Chat Timestamps"),
                       "Chat_Custom_Channels": Setting("Chat", "Custom Channels"),
                       "GUI_CompanionQuickbarExtended": Setting("GUI", "Extended Companion Quickbar"),
                       "GUI_ShowCooldownText": Setting("GUI", "Cooldown ability text"),
                       "GUI_ShowAlignment": Setting("GUI", "Show DvL Alignment"),
                       "GUI_TrackerAchievementVisible": Setting("GUI", "Achivement Tracker visable"),
                       "GUI_TrackerQuestVisible": Setting("GUI", "Mission Tracker visable"),
                       "GUI_DisciplineConfirmUnspentDialog": Setting("Confirmation", "Unspent Utility points confirmation"),
                       "GUI_DisciplineConfirmUncommittedUtilityDialog": Setting("Confirmation", "Uncommitted Utilities confirmation"),
                       "GUI_StrongholdPersonalSort": Setting("GUI", "Stronghold Sort order")}
    def __init__(self, file_path):
        self.file_path = pathlib.Path(file_path)
        self.error = False
        self.changes = False
        if not self.file_path.exists():
            self.error = True
            print("File doesnt exist")
        self.config = None
        self.name = None
        self.version = None
        #cast to path, parse version number
        try:
            self.file_name = self.file_path.parts
            self.file_name = self.file_name[len(self.file_name)-1]
            parts = str(self.file_name).split('_')
            if len(parts)>=3:
                if parts[len(parts)-1].lower()!='playerguistate.ini':
                    self.error = True
                    print("Error parsing name: {}".format(parts))
                else:
                    self.version = parts[0]
                    if len(parts)>3:
                        self.name = parts[1:len(parts)-1].join("_")
                    else:
                        self.name = parts[1]
            else:
                self.error = True
                print("Error parsing name: {}".format(parts))
            self.config = configparser.ConfigParser(delimiters="=")
            self.config.read(self.file_path)
            print(self.config.sections())
            if not ("ChatChannels" in self.config['Settings'].keys() and "GUI_Current_Profile" in self.config['Settings'].keys()):
                self.error = True
                print("Required elements not in file or error reading")
        except:
            self.error = True
            print("Unexpected error:", sys.exc_info()[0])
            print("Error Reading")
    def set(self, key, value):
        if key in self.config['Settings']:
            if self.config['Settings'][key]!=value:
                self.changes=True
                self.config['Settings'][key]=value
        else:
            self.changes=True
            self.config['Settings'][key]=value
    def has(self, key):
        return key in self.config['Settings']
    def get(self, key):
        return self.config['Settings'][key]
    def write(self):
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)
    def __str__(self):
        return "File: {}\tName: {}\tError: {}".format(str(self.file_path), self.name, self.error)
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
                if str(filename[len(filename)-1]).lower()=='ini':
                    #print()
                    self.config_files.append(pathlib.Path(self.swtor_directory/child))
        else:
            print("Directory does not exist")

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
        print(f)
    source = Swtor_Toon_Data("C:\\Users\\keepi\\AppData\\Local\\SWTOR\\swtor\\settings\\he3000_Idontdocrack_PlayerGUIState.ini")
    destination =\
        Swtor_Toon_Data("C:\\Users\\keepi\\AppData\\Local\\SWTOR\\swtor\\settings\\he3000_Isell Spice_PlayerGUIState.ini")
    for k in source.setting_mapping.keys():
        if source.has(k):
            destination.set(k, source.get(k))
    destination.write()
    #Test by coping IDDC to ISS
    #toon = Swtor_Toon_Data("C:\\Users\\keepi\\AppData\\Local\\SWTOR\\swtor\\settings\\he3000_Isell Spice_PlayerGUIState.ini")
    #print(toon)