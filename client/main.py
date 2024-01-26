import keyboard
import requests


keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))


keyboard.wait()