from flask import Blueprint, request, jsonify

from interfaces.rest_api.client import send_message
from services.conversation_service import ConversationService

class ModelRestAPI:
    def __init__(self, model_path: str):
        self.service = ConversationService()
        self.blueprint = Blueprint(model_path, __name__, url_prefix=f"/{model_path}")
        self.register_routes()

    def register_routes(self):
        @self.blueprint.post("/newsession")
        def new_session():
            data = request.get_json()
            print(f"Nova sessão: {data.get('sessionId')}")
            return jsonify({"ok": True})

        @self.blueprint.post("/endsession")
        def end_session():
            data = request.get_json()
            print(f"Fim da sessão: {data.get('sessionId')}")
            return jsonify({"ok": True})

        @self.blueprint.post("/newmessage")
        def new_message():
            data = request.get_json()
            result = self.service.execute(data["content"], data["sessionId"])

            for part, delay in zip(result.messages, result.delays):
                send_message(
                    session_id=data["sessionId"],
                    content=part,
                    duration_ms=int(delay * 1000),
                )

            return jsonify({"ok": True})