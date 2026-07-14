from flask import Flask
from config import settings
from interfaces.rest_api.server import ModelRestAPI

def start_api():
    def create_app():
        app = Flask(__name__)
        app.register_blueprint(ModelRestAPI("pinky").blueprint)
        return app

    app = create_app()
    app.run(host=settings.host, port=settings.port)

if __name__ == "__main__":
    start_api()