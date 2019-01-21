from termcolor import colored, cprint
import datetime
from pathlib import Path
from config import Config
from os import _exit

class Warrior:
    __instance = None

    @staticmethod
    def get_instance():
        if Warrior.__instance == None:
            Warrior()
        return Warrior.__instance

    def __init__(self):
        if Warrior.__instance != None:
            pass
        else:
            Warrior.__instance = self
            self.warrior_path = Config.get_instance().get_warrior_path()
            self.warriors = {}
    
    def add_warrior(self, id, ip, admin=False):
        self.warriors[id] = { "ip":ip, 
                            "isadmin":admin, 
                            "last_time": datetime.datetime.now()}
    
    def remove_warrior(self, id):
        try:
            del self.warriors[id]
            #to_del = self.warrior_path + "ibs-" + id
            #Path(to_del).unlink()
        except Exception as e:
            print(e)
        
    def kill_warriors(self):
        cprint('[+] Killing warriors...', 'green')
        for p in Path(self.warrior_path).glob("ibs-*"):
            p.unlink()

        cprint('[+] Exit...', 'green')
        _exit(-1)
    
    def get_warriors(self):
        return self.warriors

    def print_warriors(self):
        for warrior in self.warriors:
            ad = "*" if self.warriors[warrior]["isadmin"] else ""
            live = self.get_status(warrior)
            to_print = warrior + " >> " + "("+self.warriors[warrior]["ip"]+")  - " + live + " " + ad
            cprint(to_print, "yellow")
       
            
    def review_status(self, warrior_id):
        self.warriors[warrior_id]["last_time"] = datetime.datetime.now()

    def length(self):
        return len(self.warriors)

    def get_status(self, warrior_id):
        try:
            time_d = (datetime.datetime.now() - self.warriors[warrior_id]["last_time"]).seconds
            if time_d <= 15:
                live = "Alive"
            elif time_d <= 30:
                live = "Unknown"
            else:
                live = "Dead"
            return live
        except:
            return "No Exist"

    def exist_warrior(self, warrior):
        try:
            a = self.warriors[warrior]
            return True
        except:
            return False