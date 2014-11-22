from ubuntu:latest

MAINTAINER Abdul Córdoba <abdul@acm.org>

run apt-get update
run apt-get install -y git wget
run apt-get install -y xserver-xorg xdm  xfonts-base xfonts-100dpi xfonts-75dpi 
run apt-get install -y python-setuptools python-numpy python-qt4 python-scipy python-mysqldb python-lxml python-matplotlib nginx supervisor uwsgi

run apt-get install -y python-software-properties
run apt-get update
run apt-get install -y sqlite3

run wget https://raw.githubusercontent.com/abdulcordoba/Bath/e2cd085a72774393e8a66a471dbee010a9ac2d84/Scripts/req.txt
run easy_install pip
run pip install -r req.txt
run pip install uwsgi
run easy_install -U ete2
run apt-get install -y xvfb

run sed 's/DisplayManager\*authorize:.*true/DisplayManager\*authorize: false/' /etc/X11/xdm/xdm-config
run sed 's/DisplayManager\*authComplain:.*true/DisplayManager\*authComplain: false/' /etc/X11/xdm/xdm-config
