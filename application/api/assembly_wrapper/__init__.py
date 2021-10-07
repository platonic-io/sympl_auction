from assembly_client import network_client
import json

config = json.loads(open('network-config.json', 'r').read())
print(config)
network = network_client.NetworkClient()
#to be uncommented once network-client supports custom config files
#network = network_client.NetworkClient(config)
network.register_key_alias()
