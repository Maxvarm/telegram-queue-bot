#!/bin/bash

venvpath="./venv";
activatepath="$venvpath/bin/activate";
if [ ! -f $activatepath ]; then 
	python3 -m venv $activatepath;
fi
source $activatepath;
pip3 install -r requirements.txt && clear;