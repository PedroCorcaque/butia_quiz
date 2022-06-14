#!/bin/sh

# Install Pip3 
[ $(which python3-pip) ] || sudo apt install python3-pip

# Install requirements
pip3 install -r configure_install/requirements.txt

# Install nltk packages
python3 configure_install/install_nltk_files.py