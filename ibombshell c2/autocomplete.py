import os
import re
try:
    import readline
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass
import sys
from warrior import Warrior
from setglobal import Global

RE_SPACE = re.compile('.*\s+$', re.M)


class Completer(object):

    def __init__(self, commands):
        self.commands = commands
        self.setcommands = None
        self.settocomplete = None

    def setcommands(self, commands):
        self.setcommands = commands

    def set_commands_to_set(self, commands):
        self.settocomplete = commands
        
    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            if "__init__" not in name and "pyc" not in name and '~' not in name:
                path = os.path.join(root, name)
                if os.path.isdir(path):
                    name += os.sep
                res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p).replace(".py", "")
               for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p).replace(".py", "") for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_load(self, args):
        "Completions for the 'load' command."
        if not args:
            path = sys.argv[0].split('/')
            path[-1] = 'modules'
            path = "/".join(path)
            return self._complete_path(path)
        elif len(args) > 1:
            return []
        # treat the last arg as a path and complete it
        elif 'modules' in args[0] and '..' not in args[0]:
            return self._complete_path(args[-1])
        elif ' ' == args[0]:
            return ''
        # If the access is out of the actual directory, we
        # need to correct the path
        path = sys.argv[0].split('/')
        path[-1] = 'modules'
        path = "/".join(path)
        return self._complete_path(path)

    def complete_show(self, args):
        "Not doing nothing for this command right now"
        return []

    def complete_warrior(self, args):
        if len(args) > 1 and (args[0] == "rename" or args[0] == "kill"):
            return self.complete_set_warrior(args)
        my_list = [
                    option + ' ' for option in ["list", "rename", "kill"] 
                    if (option.startswith(args[0].strip(" ")) 
                    and option != args[0])
                   ]
        return my_list

    def complete_back(self, args):
        "Not doing nothing for this command right now"
        return []

    def complete_run(self, args):
        "Not doing nothing for this command right now"
        return []

    def complete_quit(self, args):
        "Not doing nothing for this command right now"
        return []

    def complete_set(self, args):
        if len(args) > 1 and args[0] == "warrior":
            return self.complete_set_warrior(args)
        my_list = [ option + ' ' for option in self.settocomplete 
                    if (option.startswith(args[0].strip(" ")) 
                        and option != args[0])]
        return my_list
    
    def complete_global(self, args):
        return self.complete_set(args)
    
    def complete_unset(self, args):
        return self.complete_set(args)
    
    def complete_unglobal(self, args):
        return self.complete_global(args)
    
    def complete_set_warrior(self, args):
        warriors = list(Warrior.get_instance().get_warriors().keys())
        return [ warrior + ' ' for warrior in warriors 
                    if (warrior.startswith(args[1].strip(" ")) 
                        and warrior != args[1])]

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in self.commands][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in self.commands:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in self.commands if c.startswith(cmd)] + [None]
        return results[state]
