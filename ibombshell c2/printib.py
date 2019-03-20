from termcolor import colored, cprint


def print_error(msg, start="", end=""):
    m = start + "[!] " + str(msg)  + end
    print_msg(m, "red")

def print_info(msg, start="", end=""):
    m = start + str(msg)  + end
    print_msg(m, "yellow")

def print_ok(msg, start="", end=""):
    m = start +"[+] " + str(msg) + end
    print_msg(m, "green")

def print_msg(msg, color):
    cprint(msg, color)