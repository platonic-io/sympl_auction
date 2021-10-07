from flask import Blueprint
from assembly_wrapper import network

static_routes = Blueprint('static_routes', __name__)

@static_routes.route('/create_user', methods=["GET", "POST"])
def create_user():
    return { "key_alias" : network.register_key_alias() }