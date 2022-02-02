#!/bin/bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source $SCRIPT_DIR/../env/bin/activate
cd $SCRIPT_DIR/../
FLASK_APP=main.py
flask run