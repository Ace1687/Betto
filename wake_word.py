import threading
import keyboard

# ---------------------------
# Hotkey listener (Ctrl+B)
# ---------------------------
def start_hotkey_listener(on_activate):
    def _listen():
        keyboard.add_hotkey("ctrl+b", on_activate)
        keyboard.wait()

    t = threading.Thread(target=_listen, daemon=True)
    t.start()
    print("Hotkey listener started — press Ctrl+B")


# ---------------------------
# Wake word listener
# ---------------------------
def start_wake_word_listener(on_activate, porcupine_key=None):

    if not porcupine_key:
        print("No Porcupine key — wake word disabled.")
        return

    try:
        import pvporcupine
        import pyaudio
        import struct

        porcupine = pvporcupine.create(
            access_key=porcupine_key,
            keywords=["bumblebee"]
        )

        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        def _listen():
            print("Listening for wake word...")
            while True:
                pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                if porcupine.process(pcm) >= 0:
                    print("Wake word detected!")
                    on_activate()

        threading.Thread(target=_listen, daemon=True).start()

    except ImportError:
        print("Missing pvporcupine or pyaudio. Install them.")
    except Exception as e:
        print(f"Wake word error: {e}")
