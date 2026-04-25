import os
import threading
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from tools import searchweb, save_to_txt, create_html_file
from betto_app import signals

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not AGENT_ID or not API_KEY:
    raise ValueError("Missing AGENT_ID or ELEVENLABS_API_KEY in .env file")

elevenlabs = ElevenLabs(api_key=API_KEY)

# ---------------------------
# REGISTER CLIENT TOOLS
# ---------------------------
client_tools = ClientTools()
client_tools.register("searchweb", searchweb)
client_tools.register("save_to_txt", save_to_txt)
client_tools.register("create_html_file", create_html_file)

conversation = None

# ---------------------------
# CALLBACKS
# ---------------------------
def on_agent_response(response):
    print(f"\nBetto: {response}")
    signals.message_received.emit("Betto", response)
    signals.set_state.emit("speaking")

def on_agent_correction(original, corrected):
    signals.message_received.emit("Betto", corrected)

def on_user_transcript(transcript):
    print(f"\nYou: {transcript}")
    signals.message_received.emit("You", transcript)
    signals.set_state.emit("thinking")

# ---------------------------
# START VOICE SESSION
# ---------------------------
def start_voice_session():
    """Starts a live voice conversation with Betto via ElevenLabs."""
    global conversation
    signals.set_state.emit("listening")

    conversation = Conversation(
        client=elevenlabs,
        agent_id=AGENT_ID,
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=on_agent_response,
        callback_agent_response_correction=on_agent_correction,
        callback_user_transcript=on_user_transcript,
        client_tools=client_tools,
    )

    def _run():
        try:
            conversation.start_session()
            conversation.wait_for_session_end()
        except Exception as e:
            print(f"Session error: {e}")
        finally:
            signals.set_state.emit("sleeping")

    threading.Thread(target=_run, daemon=True).start()

# ---------------------------
# SEND TEXT MESSAGE
# ---------------------------
def send_text_message(text):
    """
    Sends a text message to Betto.
    Uses ElevenLabs text input if session active,
    otherwise falls back to a quick one-shot voice session.
    """
    global conversation
    signals.set_state.emit("thinking")

    if conversation:
        try:
            conversation.send_user_message(text)
            return
        except Exception:
            pass

    # No active session — start one with the text as the opener
    start_voice_session()

# ---------------------------
# END SESSION
# ---------------------------
def end_session():
    global conversation
    if conversation:
        try:
            conversation.end_session()
        except:
            pass
    signals.set_state.emit("sleeping")
