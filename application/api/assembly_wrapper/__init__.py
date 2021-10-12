from assembly_client import network_client
import json

config = json.loads(open('network-config.json', 'r').read())
network = network_client.NetworkClient()
#to be uncommented once network-client supports custom config files
#network = network_client.NetworkClient(config)
