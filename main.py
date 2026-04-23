import os
import sys
from dotenv import load_dotenv

from betto_app import run_app
from wake_word import start_hotkey_listener, start_wake_word_listener
import agent

load_dotenv()

# ---------------------------
# ACTIVATE BETTO
# ---------------------------
def activate_betto():
    print("\n🤖 Betto activated!")
    agent.start_voice_session()

# ---------------------------
# HANDLE TEXT INPUT
# ---------------------------
def on_user_typed(text):
    return agent.send_text_message(text)

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    print("🤖 Starting Betto...")

    porcupine_key = os.getenv("PORCUPINE_KEY")

    # Start listeners
    start_hotkey_listener(activate_betto)
    start_wake_word_listener(activate_betto, porcupine_key)

# Start app
app, window = run_app(on_user_message=on_user_typed)
sys.exit(app.exec())