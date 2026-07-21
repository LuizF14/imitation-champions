import argparse
import subprocess
import sys
from pathlib import Path

from interfaces.streamlit_app import start_streamlit
from interfaces.rest_api.api import start_api
from services.judgement_service import JudgmentService

project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from interfaces.console import start_console
from services.persona_service import generate_personas, save_personas

def handle_generate(args):
    print(f"Starting generation of {args.quantity} new persona(s)...")
    try:
        personas = generate_personas(args.quantity)
        print(f"Saving into: {args.output}...")
        save_personas(personas, path=args.output, append=args.append)
        print("Process successfully concluded")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_test_ai(args):
    service = JudgmentService()

    result = service.run_benchmark(
        n_conversations=args.conversations,
        turns_per_conversation=args.turns,
        output_file="resources/judgement.json"
    )

    print(result.summary())

def handle_console_chat(args):
    start_console()

def handle_streamlit_chat(args):
    script_path = Path(__file__).parent / "interfaces" / "streamlit_app.py"
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(script_path)],
        check=True,
    )

def handle_rest_api(args):
    start_api()

def main():
    parser = argparse.ArgumentParser(
        description="Imitation Champions - Control CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(
        dest="command", 
        required=True, 
        help="Command to be run"
    )

    parser_generate = subparsers.add_parser("generate", help="Generate new synthetic personas")
    parser_generate.add_argument(
        "-n", "--quantity", type=int, default=3, 
        help="Amount of new personas to generate"
    )
    parser_generate.add_argument(
        "-o", "--output", type=str, default="data/personas.json", 
        help="Output file path"
    )
    parser_generate.add_argument(
        "--no-append", action="store_false", dest="append", 
        help="Overwrite instead of appending"
    )
    parser_generate.set_defaults(func=handle_generate)

    parser_chat = subparsers.add_parser("console-chat", help="Start a new conversation in the terminal")
    parser_chat.set_defaults(func=handle_console_chat)

    parser_chat = subparsers.add_parser("streamlit-chat", help="Start a new conversation in the streamlit frontend")
    parser_chat.set_defaults(func=handle_streamlit_chat)

    parser_chat = subparsers.add_parser("test-ai", help="Use a judge agent to test the ai")
    parser_chat.add_argument(
        "-c", "--conversations", type=int, default=10, 
        help="Amount of conversations to evaluate"
    )
    parser_chat.add_argument(
        "-t", "--turns", type=int, default=6, 
        help="Amount of turns per conversation"
    )
    parser_chat.set_defaults(func=handle_test_ai)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()