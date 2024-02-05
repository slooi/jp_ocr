from typing import Dict, Mapping, cast
import requests
import keyboard
import pathlib
import base64
import json
import io
from PIL import Image
import requests
import mss.tools

from typing import Union
from pydantic import BaseModel

DEBUG_MODE = True

# keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))
# keyboard.wait()


from typing import TypedDict


class KnownError(Exception):
	pass

class TwoPoints(BaseModel):
	x1: int
	y1: int
	x2: int
	y2: int


def post_image(url: str, image_arg: pathlib.Path | bytes):
	# Check input argument
	if type(image_arg) == bytes:
		# print("image_arg is bytes")
		im_bytes = image_arg
	else:
		# print("image_arg is path:", image_arg)
		with open(image_arg, "rb") as f:
			im_bytes = f.read()

	try:
		# Send post request
		response = requests.post(
			url,
			files={"image2": ("toOCR.jpg", io.BytesIO(im_bytes), "image/jpeg")},
			timeout=5,
		)
	except Exception as e:
		raise KnownError(e)

	# Process response
	try:
		data = response.json()
		print("Response Data:\n{}".format(data))
	except requests.exceptions.RequestException as e:
		raise KnownError(e)


class RectangularShape(BaseModel):
	top: int
	left: int
	width: int
	height: int


def calc_rectangular_shape(two_points: TwoPoints) -> RectangularShape:
	two_points2 = two_points.model_dump()
	if two_points2["x1"] == two_points2["x2"] or two_points2["y1"] == two_points2["y2"]:
		raise ValueError("ERROR: Width AND height must both have a length > 0")

	top, left, width, height = 0, 0, 0, 0

	# Calculate vertical
	if two_points2["y1"] < two_points2["y2"]:
		top = two_points2["y1"]
		height = two_points2["y2"] - two_points2["y1"]
	else:
		top = two_points2["y2"]
		height = two_points2["y1"] - two_points2["y2"]

	# Calculate horizontal
	if two_points2["x1"] < two_points2["x2"]:
		left = two_points2["x1"]
		width = two_points2["x2"] - two_points2["x1"]
	else:
		left = two_points2["x2"]
		width = two_points2["x1"] - two_points2["x2"]

	return RectangularShape(
		width=round(width), height=round(height), left=round(left), top=round(top)
	)


def capture_screen(screen_area: Union[RectangularShape, TwoPoints]):
	with mss.mss() as sct:
		# Check
		if isinstance(screen_area, RectangularShape):
			monitor = screen_area.model_dump()  # cast to mapping
		elif isinstance(screen_area, TwoPoints):
			monitor = calc_rectangular_shape(
				screen_area
			).model_dump()  # cast to mapping

		# monitor_dict = {key: int(value) if isinstance(value, (int, float)) else 0 for key, value in screen_area.items()}
		# monitor: Mapping = screen_area
		sct_img = sct.grab(monitor)

		#
		img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
		img_bytes = io.BytesIO()
		img.save(img_bytes, format="jpeg")

		# Save to the picture file
		if DEBUG_MODE:
			print("___DEBUG: Saved screenshot to file___")
			# print(output)
			# with open("debug.capture_screen.jpg", "wb") as f:
			#     f.write(img_bytes.read())
			img.save("debug.capture_screen.jpg", format="jpeg")

		# MAKE SURE TO RESET THE SEEK POINTER AFTER READS
		img_bytes.seek(0)

		return img_bytes.read()


if __name__ == "__main__":
	post_image(
		"http://localhost:54321/",
		capture_screen(TwoPoints(x1=0, y1=0, x2=100, y2=1000)),
	)


# post_image('http://localhost:54321/',pathlib.Path("assets","edit.jpg"))

# post_image('http://localhost:54321/',capture_screen(calc_rectangular_shape({"x1":0,"y1":0,"x2":300,"y2":1080})))
# capture_screen()

# post_image('http://localhost:54321/',pathlib.Path("asdas.jpg"))
