# terminal scans

This is the terminal endpoint application for BDDW.

# installation

install/enable wsl on windows endpoint
install ubuntu 20.04
You may have to run wsl_update_x64.msi to update wsl kernel

create user bddw
install docker
install docker-compose

sudo apt-get updates
sudo apt-get upgrade


# configuration

remove pw prompt for root
https://www.simplehelp.net/2009/05/27/how-to-stop-ubuntu-from-asking-for-your-sudo-password


mkdir /home/bddw/django-projects/
cd django-projects
git clone https://github.com/dev-bddw/terminal_scans.git
Set .envs/.local/.scans:
    APP_KEY=<API KEY HERE>
    LOCATION_CODE=101

cp /home/bddw/django-projects/terminal_scans/wsl-init /etc/wsl-init

# schedule tasks to run wsl & start docker at localhost:8000 on startup

TASK ONE "START WSL"
    Run wsl.exe at system startup
    Run whether user is logged in or not
    Do not store password

TASK TWO "START TERMINAL SCANS"
    At log on
    Program/script: wsl
    Add arguments: -d Ubuntu-20.04 -u bddw /etc/init-wsl

# last
In wsl make script executable
sudo chmod +x /etc/init-wsl
