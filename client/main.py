import requests
import keyboard
import pathlib



import base64
import json           
import io
from PIL import Image

import requests


import mss.tools

DEBUG_MODE = True

# keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))
# keyboard.wait()


def post_image(url:str,image_arg:pathlib.Path|bytes):
	# Check input argument
	if type(image_arg) == bytes:
		print("image_arg is bytes")
		im_bytes = image_arg
	else:
		print("image_arg is path:",image_arg)
		with open(image_arg, "rb") as f:
			im_bytes = f.read()

	# Send post request
	response = requests.post(url, files={'image2': ('toOCR.jpg', io.BytesIO(im_bytes), 'image/jpeg')},timeout=5)

	# Process response
	try:
		data = response.json()
		print(data)
	except requests.exceptions.RequestException:
		print(response.text)
		


def capture_screen():

	with mss.mss() as sct:
		# The screen part to capture
		monitor = {"top": 0, "left": 0, "width": 300, "height": 1080}
		output = str(pathlib.Path(".assets","sct-{top}x{left}_{width}x{height}.png".format(**monitor)))

		# Grab the data
		sct_img = sct.grab(monitor)

		# 
		img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
		img_bytes = io.BytesIO()
		img.save(img_bytes, format="jpeg")
		img_bytes.seek(0)
		
		# Save to the picture file
		if DEBUG_MODE:
			print("___DEBUG: Saved screenshot to file___")
			print(output)
			with open("debug.capture_screen.jpg","wb") as f:
				f.write(img_bytes.read())
	
		return img_bytes.read()
	


# post_image('http://localhost:54321/',pathlib.Path("assets","edit.jpg"))

post_image('http://localhost:54321/',capture_screen())
# capture_screen()

# post_image('http://localhost:54321/',pathlib.Path("asdas.jpg"))