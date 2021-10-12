from flask import Flask
from routes.static import static_routes
from routes.generated import generated_routes

app=Flask(__name__)
app.register_blueprint(static_routes)
app.register_blueprint(generated_routes)
