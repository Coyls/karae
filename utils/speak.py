
import subprocess

import gtts
from playsound import playsound

class Speak:

    def speak(txt: str):
        subprocess.run(["sh","./scripts/speak.sh",txt])

    def speakGtts(txt: str):
        tts = gtts.gTTS(txt, lang="fr")
        tts.save("./audio/txt.mp3")
        playsound("./audio/txt.mp3")

