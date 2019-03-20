from termcolor import colored


# Commands >> 'load', 'set', 'unset', 'global', 'show', 'run', 'back', 'warrior', 'quit', 'help'
def show_help():
        help = "\n"
        help += colored('load <module>\n', 'yellow')
        help += "-------------\n"
        help += "|_ Load a specific module"
        help += "\n\n"

        help += colored('back\n', 'yellow')
        help += "----\n"
        help += "|_ Unload a module"
        help += "\n\n"           

        help += colored('show\n', 'yellow')
        help += "----\n"
        help += "|_ Show module info and options"
        help += "\n\n"

        help += colored('set <option> <value>\n', 'yellow')
        help += "--------------------\n"
        help += "|_ Assign value to an option"
        help += "\n\n"

        help += colored('unset <option>\n', 'yellow')
        help += "--------------\n"
        help += "|_ Set null an option"
        help += "\n\n"

        help += colored(' global <option> <value>\n', 'yellow')
        help += "-----------------------\n"
        help += "|_ Assign value to a global option"
        help += "\n\n"          

        help += colored('run\n', 'yellow')
        help += "---\n"
        help += "|_ Start the module"
        help += "\n\n"

        help += colored('warrior list / rename / kill\n', 'yellow')
        help += "----------------------------\n"
        help += "|_ Use it to show, rename or kill warriors"
        help += "\n\n"

        help += colored('help\n', 'yellow')
        help += "----\n"
        help += "|_ Show this text"
        help += "\n\n"

        help += colored('# system_command\n', 'yellow')
        help += "----\n"
        help += "|_ Executes a command on the local system"
        help += "\n\n"

        help += colored('quit\n', 'yellow')
        help += "----\n"
        help += "|_ Leave iBombShell :("
        help += "\n"
        
        print(help)