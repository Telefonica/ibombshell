from termcolor import colored, cprint


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
            self.warriors = {}
    
    def add_warrior(self, id, ip, admin=False):
        self.warriors[id] = { "ip":ip, 
                            "isadmin":admin, 
                            "isalive":True}
    
    def remove_warrior(self, id):
        try:
            del self.warriors[id]
        except Exception as e:
            print(e)
    
    def get_warriors(self):
        return self.warriors

    def print_warriors(self):
        for warrior in self.warriors:
            ad = "*" if self.warriors[warrior]["isadmin"] else ""
            live = "Live" if self.warriors[warrior]["isalive"] else "Death"
            to_print = warrior + " >> " + "("+self.warriors[warrior]["ip"]+")  - " + live + " " + ad
            cprint(to_print, "yellow")

    def length(self):
        return len(self.warriors)