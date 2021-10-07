from flask import Flask
from routes.static import static_routes

app=Flask(__name__)
app.register_blueprint(static_routes)

