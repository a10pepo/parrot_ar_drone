#!/bin/bash

echo "#########################"
echo "## START INSTALLATION ##"
echo "#########################"
echo "##################################"
echo "## INSTALLATION OLYMPLE PARROT ##"
echo "##################################"


git config --global user.email $0;
git config --global user.name $1;
cd $HOME; mkdir -p code/parrot-groundsdk; 
cd code/parrot-groundsdk; apt install --yes repo;
repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git;
repo sync; ./products/olympe/linux/env/postinst;
./build.sh -p olympe-linux -A all final -j;

echo "##################################"
echo "## INSTALLATION SPHINX PARROT  ##"
echo "##################################"

echo "deb http://plf.parrot.com/sphinx/binary `lsb_release -cs`/" | sudo tee /etc/apt/sources.list.d/sphinx.list > /dev/null;
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 508B1AE5;
sudo apt-get update;
sudo apt install --yes mesa-utils;
sudo apt-get install --yes parrot-sphinx;
sudo systemctl start firmwared.service;
sphinx /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::stolen_interface=::simple_front_cam=true

