import sys
import uuid

from services.conversation_service import ConversationService

def start_console():
    try:
        service = ConversationService()
    except Exception as e:
        print(f"Failure: {e}", file=sys.stderr)
        sys.exit(1)

    thread_id = f"console-{uuid.uuid4().hex[:8]}"
    print(f"Pinky console — thread_id: {thread_id} — /exit to quit")

    while True:
        message = input("\n[User]: ").strip()
        if message.lower() in ("/exit"):
            break
        if not message:
            continue

        result = service.execute(message, thread_id)
        for part in result.messages:
            print(f"[Bot]: {part}")