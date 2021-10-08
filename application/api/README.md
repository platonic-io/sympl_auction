# Sympl_Auction API Server

This is the api server to provide a clean interface for the Sympl Auction. It is created in python with a python client, and everything can be run and installed in a virtual enviornment. The web framework chosen for this project is Flask.

This api server has been tested on python3.9, and confirmed works with this version.

# Building

A convenient build script has been provided for you, you can run the `build.sh` script to create the python virtual enviornment, install dependencies, and start up a sandbox on which to run the auction contract. If you would like to run more python commands in the virtualenv, you can do so by running `source ./env/bin/activate`. The build script requires the Assembly SDK (>v2.0.1) to be installed. This can be downloaded using our `symenv` tool. 

# Running

The server can be run by running the `start.sh` script, which automatically sources `./env/bin/activate` and then runs the default flask run. Any options you can supply to flask run are supported

# Resetting
You can reset the enviornment by running the script `reset.sh`. This will remove the virtual environment, and stop the created sandox network.
# Api Routes

All routes which get forwarded to assembly require a header to be set: `user: <KeyAlias>` this is the key alias who will be performing the action of the smart contract. The header for `ContentType` must also be set to `application/json`, otherwise the api server will not understand the data it is receiving.

All these routes are located at `POST /<function_name>`, and the JSON data that gets POSTED to them will be the parameters of each @clientside function located in `auction.sympl`

Additionally, there is a route called `POST /create_user` which will register a key alias on the node to be used to make contract function calls. Each key alias corresponds to a different user. 