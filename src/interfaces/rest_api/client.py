import logging

import requests

from config import settings

logger = logging.getLogger("pinky.client")


def send_message(session_id: str, content: str, duration_ms: int) -> bool:
    try:
        response = requests.post(
            f"{settings.backend_url}/api/messageproduced/{session_id}",
            json={
                "content": content,
                "creationDurationMs": duration_ms,
            },
            headers={"x-api-key": settings.imitation_api_key},
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Falha ao enviar mensagem (session={session_id}): {e}")
        return False