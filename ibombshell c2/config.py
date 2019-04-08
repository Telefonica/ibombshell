import json

class Config:
    __instance = None
    __config = {}

    @staticmethod
    def get_instance():
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance == None:
            Config.__instance = self
            self.__load_config()

    def __load_config(self):
        try:
            with open("config.json") as config:
                self.__config = json.load(config)
        except:
            self.__config["warrior_path"] =  "/tmp/"
        
        # Path must to end in /
        if not self.__config["warrior_path"].endswith("/"):
             self.__config["warrior_path"] = self.__config["warrior_path"] + "/"
    
    def get_config(self):
        return self.__config
    
    def get_warrior_path(self):
        return self.__config["warrior_path"]