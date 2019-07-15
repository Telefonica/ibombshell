from module import Module
from termcolor import colored, cprint

class CustomModule(Module):
    def __init__(self):

        information = {"Name": "tcpscan",
                       "Description": "TCP Portscan for ibombshell",
                       "License": "BSD 3-Clause",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "ip": ["127.0.0.1", "Host to scan", True],
                   "ports": ["20-500", "Ports to scan. examples 80 or 20-500", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function tcp-scan{
    param(
        [switch]$range,
        [string]$ip,
        [ValidateRange(1,65535)]
        [int]$port,
        [int]$begin,
        [int]$end
    )
    $res = Test-Connection $ip  -Count 1 -ErrorAction SilentlyContinue
    if (-not $res) { 
        return "That IP is not alive"
    } 
    if($range)
    { 
        $pool = [RunspaceFactory]::CreateRunspacePool(1, 100)
        $pool.open()
        $runspaces = @()
        if($begin -le $end)
        {
            for($p=$begin; $p -le $end; $p++){
                $runspace = [powershell]::create()

                $null = $runspace.addscript($check_connection)
                $null = $runspace.addargument($ip)
                $null = $runspace.addargument($p)

                # Create new runspace
                $runspace.runspacepool = $pool
                $runspaces += @{pipe=$runspace; Status=$runspace.begininvoke()}
            }

            # Wait all runspaces
            while ($runspaces.status -ne $null)
            {
                $finished = $runspaces | where { $_.status.iscompleted -eq $true };
                
                # Clear completed tasks
                foreach ($runspace in $finished)
                {
                    $runspace.pipe.endinvoke($runspace.status)
                    $runspace.status = $null            
                }
            }

            $pool.close();
            $pool.dispose();
        }
    }
    elseif($port)
    { 

         try
        {
            (New-Object System.Net.Sockets.TcpClient).Connect($ip, $port)
        }
        catch
        {

        }
        $msg = "Port:$port is not open"  
        if(echo $?)
        {
            $msg = "Port:$port is open"               
        } 
        return $msg
    }
}


$check_connection = {
        param ([string]$ip, [int]$port);
    $tcp_client = new-Object system.Net.Sockets.TcpClient         
    $conn = $tcp_client.BeginConnect($ip, $port, $null, $null) 
    $ok = $conn.AsyncWaitHandle.WaitOne(1000,$false) 
    if ($ok) {
        $error.clear()
        $tcp_client.EndConnect($conn) | out-Null 
        if (-not $Error[0]) {
            return "Port:$port is open"
        }
    }
 }
 """
        ports = self.args["ports"].split("-")
        if len(ports) >= 2:
            function += 'tcp-scan -ip {} -range -begin {} -end {}'.format(self.args["ip"], ports[0], ports[1])
        else:
            function += 'tcp-scan -ip {} -port {}'.format(self.args["ip"], ports[0])

        super(CustomModule, self).run(function)