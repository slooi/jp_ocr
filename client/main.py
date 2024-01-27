import keyboard
import requests
import pathlib

# keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))
# keyboard.wait()

import base64
import json           
import io         

import requests

api = 'http://localhost:54321/'
image_file = pathlib.Path("assets","edit.jpg")

with open(image_file, "rb") as f:
    im_bytes = f.read()        

# headers = {'Content-type': 'multipart/form-data', 'Accept': 'text/plain'}
response = requests.post(api, files={'image': ('edit.jpg', io.BytesIO(im_bytes), 'image/jpeg')},timeout=5)
try:
    data = response.json()     
    print(data)                
except requests.exceptions.RequestException:
    print(response.text)
    
