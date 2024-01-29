import requests
import keyboard
import pathlib




# keyboard.add_hotkey('ctrl+shift+a', lambda:requests.get("http://localhost:54321"))
# keyboard.wait()


print("hgj hj kh")

# import base64
# import json           
# import io         

# import requests

# api = 'http://localhost:54321/'
# image_file = pathlib.Path("assets","edit.jpg")

# with open(image_file, "rb") as f:
#     im_bytes = f.read()        

# # headers = {'Content-type': 'multipart/form-data', 'Accept': 'text/plain'}
# response = requests.post(api, files={'image2': ('toOCR.jpg', io.BytesIO(im_bytes), 'image/jpeg')},timeout=5)
# try:
#     data = response.json()     
#     print(data)                
# except requests.exceptions.RequestException:
#     print(response.text)
    




import mss.tools

with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)
    

