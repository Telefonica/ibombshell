from termcolor import colored, cprint
from module import Module


class CustomModule(Module):

    def __init__(self):
        information = {"Name": "Unquoted Service Path",
                       "Description": "Obtain the services that have the route without quotation marks and with blank spaces",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function unquoted-service-path{
    $services =  sc.exe query type= service

    $found = $false
    $result = ""
    foreach($service in $services){
        if ($service.contains("SERVICE_NAME") -or $service.contains("NOMBRE_SERVICIO")){
            $name = $service.split(":")[1].TrimStart().TrimEnd()
            $data = sc.exe qc $name
            $s_name = $name
            $s_path = ""
            $s_start = ""
            
            foreach($d in $data){
             
                if (($d.contains("BINARY_PATH_NAME") -or $d.contains("NOMBRE_RUTA_BINARIO")) -and (-not $d.contains('"'))) {

                    $aux = $d.replace("BINARY_PATH_NAME: ", "")
                    $aux = $aux.replace("NOMBRE_RUTA_BINARIO: ", "")
                    $aux2 = $aux.split("-k")[0].TrimStart().TrimEnd()
                    $aux3 = $aux2.split("/")[0].TrimStart().TrimEnd()

                    if ($aux3.contains(" ")){
                        $s_path = $aux3
                    }

                }
                if ($d.Contains("SERVICE_START_NAME") -or $d.Contains("NOMBRE_INICIO_SERVICIO")) {
                    $s_start = $d
                }
            }

            if ($s_path){
                $found = $true
                $result =  $result + $s_name + " >> " +  $s_path + "\n"
            }
        }

    }
    if (-not $found){
        $result = "No found services with path 'vulnerable'"
    }
    return $result
}
            """

        function += "unquoted-service-path"
        super(CustomModule, self).run(function)