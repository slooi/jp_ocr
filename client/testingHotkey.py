from typing import Any, Dict, List, TypedDict, Union, Callable
from pydantic import BaseModel
from pynput import keyboard
"""
############### NORMAL  => q
key: q
key.vk: 51

############### SPECIAL  => left alt
key.name: alt_l
key.value.vk: 164
"""

class Hotkey(BaseModel): # type: ignore
    modifiers: List[int]
    key: int
    callback: Callable[[],None]

class HotkeyHandler():
	""" 
		This class handles the calling hotkeys and suppression of keys

		METHODS:
		add_hotkey_vk()
		start()

		EXAMPLE USAGE:
		hotkeyHandler = HotkeyHandler()
		hotkeyHandler.add_hotkey_vk("192")

		NOTES:
		- When a ALL REGISTERED modifer keys of a hotkey is being pressed, if said hotkey's normal key is pressed it is suppressed so the currently focused program is not affected (eg: notepad).

	"""

	def __init__(self,hotkeys:List[Hotkey]) -> None:
		# (160, 'shift'), (162, 'ctrl_l'), (91, 'cmd' THIS ALSO THE WIN KEY), (164, 'alt_l'), (165, 'alt_gr'), (161, 'shift_r'), (163, 'ctrl_r')
		self.modifier_vks = (160, 162, 91, 164, 165, 161, 163)

		""" 
		hotkey: win+shift+`

		if win + ` is pressed 		=>		` NOT SUPPRESSED
		if win + shift + `			=>		` suppressed
		"""

		""" 
		hotkeys:[
			{
				modifiers: []
				key:
				callback:
			} 
		]
		"""
		self.hotkeys = hotkeys
		self.keys_pressed:Dict[int,bool] = {}

		self.KEY_DOWN = 256
		self.KEY_UP = 257

	
	
	def setup(self):
		def setup_listener():
			listener:Union[None,keyboard.Listener] = None
			def on_press(key):
				if hasattr(key,"vk"):
					print(key.vk)
				else:
					print(key.value.vk)

			def on_release(key):
				if key == keyboard.Key.num_lock:
					# Stop listener
					return False
				
			def win32_event_filter(msg, data):
				# Check if key has just been pressed or released
				if (msg == self.KEY_DOWN or msg == self.KEY_UP):

					# Prevent OTHER PROGRAMS from sensing this key press
					if listener: listener._suppress = True
					# if you return False, your on_press/on_release will not be called
				
				return True

			# Collect events until released
			listener =  keyboard.Listener(
					on_press=on_press,
					on_release=on_release, # type: ignore
					win32_event_filter=win32_event_filter)
			return listener

		with setup_listener() as l:
			l.join()


HotkeyHandler([Hotkey(modifiers=[91],key=192,callback=lambda:print("hi"))])


