from flask import Flask
from config import settings
from interfaces.rest_api.server import ModelRestAPI

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ModelRestAPI("pinky").blueprint)
    return app

app = create_app()

def start_api():
    app.run(host=settings.host, port=settings.port)

if __name__ == "__main__":
    start_api()