FROM mcr.microsoft.com/powershell

RUN apt-get update && \
	apt-get -y install python3 git python3-pip

RUN git clone https://github.com/Telefonica/ibombshell

RUN chmod -R 755 /ibombshell
WORKDIR /ibombshell

RUN pip3 install -r ibombshell\ c2/requirements.txt

CMD pwsh -C "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/Telefonica/ibombshell/master/console');console;/bin/bash"

