#!/bin/bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
#set -eo pipefail

python3 -m virtualenv $SCRIPT_DIR/../env
source $SCRIPT_DIR/../env/bin/activate

NETWORK_NAME=default

echo "--Finding Assembly Client"
ASSEMBLY_CLIENT_WHEEL=$(find $HOME/.symbiont/versions/current/assembly_client | grep .whl | tail -n 1)
REQUIREMENTS_WITHOUT_ASSEMBLY_CLIENT=$(cat $SCRIPT_DIR/../requirements.txt | grep -v assembly_client)
echo -e "$REQUIREMENTS_WITHOUT_ASSEMBLY_CLIENT" > $SCRIPT_DIR/../requirements.txt
echo -e "assembly_client @ file://$ASSEMBLY_CLIENT_WHEEL" >> $SCRIPT_DIR/../requirements.txt

echo "--Installing Pip Requirements"
pip install -r $SCRIPT_DIR/../requirements.txt

echo "--Starting Network and generating files"
sym sandbox start

sym network publish -c $HOME/.symbiont/assembly-dev/mock-network/$NETWORK_NAME/network-config.json -d $SCRIPT_DIR/../../../
ln -sf $HOME/.symbiont/assembly-dev/mock-network/$NETWORK_NAME/network-config.json $SCRIPT_DIR/../network-config.json

sym generate -i $SCRIPT_DIR/../routes/template -o $SCRIPT_DIR/../routes/generated
rm $SCRIPT_DIR/../routes/generated/lib.js