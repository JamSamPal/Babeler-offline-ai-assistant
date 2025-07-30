from assistant.python.offline_assistant import Assistant
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the assistant.")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Run assistant in text-only mode (no mic or speaker)."
    )

    args = parser.parse_args()

    if args.text:
        assistant = Assistant(soundless=True)
    else:
        assistant = Assistant()

    assistant.main()

if __name__ == "__main__":
    main()