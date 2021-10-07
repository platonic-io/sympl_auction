set -eo pipefail

python3 -m virtualenv env
source ./env/bin/activate

NETWORK_NAME=default

echo "--Installing Pip Requirements"
pip install -r requirements.txt

echo "--Starting Network and generating files"
sym sandbox start

sym network publish -c $HOME/.symbiont/assembly-dev/mock-network/$NETWORK_NAME/network-config.json -d ../../
ln -sf $HOME/.symbiont/assembly-dev/mock-network/$NETWORK_NAME/network-config.json network-config.json