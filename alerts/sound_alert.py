# alerts/sound_alert.py

import winsound
import threading


def play_alert():

    def _beep():
        try:
            winsound.Beep(1000, 500)
        except Exception as e:
            print(f"[ALERT ERROR] {e}")

    threading.Thread(
        target=_beep,
        daemon=True
    ).start()