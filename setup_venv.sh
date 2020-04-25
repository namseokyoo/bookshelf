#!/bin/bash
sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-pip

python3 -m venv .venv
source ./.venv/bin/activate
