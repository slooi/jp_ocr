import requests
import keyboard
import pathlib



import base64
import json           
import io         

import requests


import mss.tools

DEBUG_MODE = True

# keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))
# keyboard.wait()


def post_image(url:str,image_path:pathlib.Path):
	with open(image_path, "rb") as f:
		im_bytes = f.read()

	response = requests.post(url, files={'image2': ('toOCR.jpg', io.BytesIO(im_bytes), 'image/jpeg')},timeout=5)
	try:
		data = response.json()
		print(data)
	except requests.exceptions.RequestException:
		print(response.text)
		

post_image('http://localhost:54321/',pathlib.Path("assets","edit.jpg"))

def capture_screen():

	with mss.mss() as sct:
		# The screen part to capture
		monitor = {"top": 0, "left": 0, "width": 300, "height": 300}
		output = str(pathlib.Path(".assets","sct-{top}x{left}_{width}x{height}.png".format(**monitor)))
		print("output",output)

		# Grab the data
		sct_img = sct.grab(monitor)

		# Save to the picture file
		if DEBUG_MODE:
			mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
			print("___DEBUG: Saved screenshot to file___")
		print(output)
	

