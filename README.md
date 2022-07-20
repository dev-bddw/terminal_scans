terminal scans
---------------

This is the terminal endpoint application for BDDW.

# installation

install/enable wsl on windows endpoint

in powershell w/ admin priv:

> wsl.exe --install

open remove programs and remove whatever distro windows installed

install ubuntu 20.04 from microsoft app store
You may have to run wsl_update_x64.msi to update wsl kernel

sudo apt-get updates
sudo apt-get upgrade


create user bddw
install docker
install docker-compose

sudo apt-get updates
sudo apt-get upgrade


# remove pw prompt for bddw user

sudo visudo
at buttom
bddw ALL=(ALL) NOPASSWD: ALL

# clone repo

mkdir /home/bddw/django-projects/
cd django-projects
git clone https://github.com/dev-bddw/terminal_scans.git

# config local settings

touch /home/bddw/django-projects/.envs/.local/.scans
sudo vim /home/bddw/django-projects/.envs/.local/.scans

Set .envs/.local/.scans:
    APP_KEY=<API KEY HERE>
    LOCATION_CODE=<LOCATION_CODE>

# copy bash script from

cp /home/bddw/django-projects/terminal_scans/wsl-init /etc/wsl-init

# make it executable

sudo chmod +x /etc/wsl-init

# schedule tasks to run wsl & start docker at localhost:8000 on startup

Add tasks from one drive task folder
RUN WSL -- start wsl.exe any user on startup
START TERMINAL SCANS -- start bash script any user on startup

# ALL DONE



# last
In wsl make script executable
sudo chmod +x /etc/init-wsl
