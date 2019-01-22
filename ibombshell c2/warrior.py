from termcolor import colored, cprint
import datetime
from pathlib import Path
from config import Config
from os import _exit, rename
from time import sleep

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
        if self.length() == 0:
                cprint('[!] Warriors haven\'t been found...', 'red')
        else:
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
    
    def get_warrior_path(self,warrior):
        try:
            self.warriors.get(warrior)
            return self.warrior_path + "ibs-" + warrior
        except:
            return None
    
    def rename_warrior(self, warrior): 
        path_to_rename = self.get_warrior_path(warrior)
        if path_to_rename:
            new_name = ""
            while not new_name:
                new_name = input("Write the new name: ")
                        
            with open(path_to_rename, 'a') as f:
                f.write("$id = '{}'".format(new_name))          
            cprint("Renaming ... ", "yellow")
            sleep(5)
            w = self.warriors[warrior]
            self.warriors[new_name] = w
            self.remove_warrior(warrior)
            new_path = path_to_rename.split("ibs-")[0] + "ibs-" + new_name
            rename(path_to_rename, new_path)
            cprint("[+] Done ", "green")
    
    def kill_warrior(self, warrior):
        path_to_kill = self.get_warrior_path(warrior)
        if path_to_kill:                        
            with open(path_to_kill, 'a') as f:
                f.write("$global:condition = $false")          
            cprint("Killing ... ", "yellow")
            sleep(5)
            self.remove_warrior(warrior)
            cprint("[+] Done ", "green")
        