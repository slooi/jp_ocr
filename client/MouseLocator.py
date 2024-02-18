from pynput.mouse import Listener, Controller
from pynput.keyboard import Listener as KeyboardListener, Key

# Instantiate a mouse controller object
mouse = Controller()
mouse_x, mouse_y = 0,0

# Function to get and print the current mouse position
def on_move(x, y):
	global mouse_x, mouse_y
	mouse_x = x
	mouse_y = y
	
	# print('Mouse moved to {0}'.format((x, y)))

# Function to detect key presses
def on_press(key):
	try:
		if key.char == 'p':
			print("mouse_x,mouse_y:",mouse_x,mouse_y)
	except:
		pass

# Create a listener for mouse events
with Listener(on_move=on_move) as mouse_listener:
	# Create a listener for keyboard events
	with KeyboardListener(on_press=on_press) as keyboard_listener:
		mouse_listener.join()
		keyboard_listener.join()


""" 
pppppppppp
pppppppppppppppppppp
 """