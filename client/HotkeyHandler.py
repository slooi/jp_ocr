from typing import Any, Dict, List, TypedDict, Union, Callable
from pydantic import BaseModel
from pynput import keyboard
"""
############### NORMAL KEY EVENT ### eg: q
key: q
key.vk: 51
############### SPECIAL KEY EVENT ### eg: left alt
key.name: alt_l
key.value.vk: 164
"""

class Hotkey(BaseModel): # type: ignore
	modifiers: List[int]
	key: int
	callback: Callable[[],None]

class HotkeyHandler():
	""" 
		This class handles the calling of hotkeys and suppression of keys

		EXAMPLE USAGE:
		hotkeyHandler = HotkeyHandler()
		hotkeyHandler.add_hotkey_vk("192")

		EXAMPLES:
			hotkey: win+shift+`

			if win + ` is pressed 		=>		` NOT SUPPRESSED
			if win + shift + `			=>		` suppressed

		NOTES:
		- When a ALL REGISTERED modifier keys of a hotkey is being pressed, if said hotkey's normal key is pressed it is suppressed so the currently focused program is not affected (eg: notepad).
	"""

	def __init__(self,hotkeys:List[Hotkey]) -> None:
		""" 
		hotkeys:[
			{
				modifiers: []
				key:
				callback:
			} 
		]
		"""
		self.hotkeys:List[Hotkey] = hotkeys
		self.keys_pressed:Dict[int,bool] = {}


class WindowsHotkeyHandler(HotkeyHandler):
	# (160, 'shift'), (162, 'ctrl_l'), (91, 'cmd' THIS ALSO THE WIN KEY), (164, 'alt_l'), (165, 'alt_gr'), (161, 'shift_r'), (163, 'ctrl_r')
	# self.MODIFIER_VKCS = (160, 162, 91, 164, 165, 161, 163)

	KEY_DOWN = 256
	KEY_UP = 257

	WM_SYSKEYDOWN = 0x0104
	WM_SYSKEYUP = 0x0105

	def __init__(self,hotkeys:List[Hotkey]):
		super().__init__(hotkeys)
		self.setup()


	def setup(self):
		def setup_listener():
			listener:Union[None,keyboard.Listener] = None	# WARNING: This listener is used for all hotkeys in this class. Not just one key, thus you can only suppress all keys, or no keys 

			def on_press(key): pass
			def on_release(key):
				if key == keyboard.Key.num_lock: return False # Stop listener
				
			def win32_event_filter(msg, data):


				DOWN_EVENT:bool = bool(msg == self.KEY_DOWN or msg == self.WM_SYSKEYDOWN)
				UP_EVENT:bool = bool(msg == self.KEY_UP or msg == self.WM_SYSKEYUP)

				# On windows event, check if a normal key or system key down/up event occurred
				if (DOWN_EVENT or UP_EVENT):
					code = data.vkCode

					# Update keys pressed
					self.keys_pressed[code] = DOWN_EVENT

					print("code: {}, keydown: {}".format(code,DOWN_EVENT))
					print(self.keys_pressed)

					if DOWN_EVENT:
						# 1) Iterate over all the hotkeys
						for hotkey in self.hotkeys:

							# 1.1 Check if the current key being pressed is inside the hotkey
							if not hotkey.key is code:
								if listener: listener._suppress = False
								continue

							# 1.2) Count the number of `Hotkey's modifiers` that are currently being pressed
							num_of_modifiers_pressed = 0
							for modifier in hotkey.modifiers:
								if modifier in self.keys_pressed and self.keys_pressed[modifier] == True:
									num_of_modifiers_pressed += 1
						
							# 1.3) If **ALL** the `Hotkey's modifiers` are currently being pressed, then SUPPRESS the normal key!
							if num_of_modifiers_pressed == len(hotkey.modifiers):
								if listener: listener._suppress = True # Prevent OTHER PROGRAMS from sensing this key press
								print("### SUPPRESSING KEY PRESS ###")
								break
							else:
								if listener: listener._suppress = False
								print("Modifier keys are not pressed")
					if UP_EVENT:
						# Make sure to make listener unsuppress when release ANY key. Remember the listener which listens for ALL KEYS gets suppressed, so we need to unsuppress it ASAP 
						if listener: listener._suppress = False

				return True # if you return False, your on_press/on_release will not be called

			# Collect events until released
			listener =  keyboard.Listener(
					on_press=on_press,
					on_release=on_release, # type: ignore
					win32_event_filter=win32_event_filter)
			return listener

		with setup_listener() as l:
			l.join()

""" 
### NOTES
91 - left windows key
192 - backtick(`)
``
"""
WindowsHotkeyHandler([Hotkey(modifiers=[91],key=192,callback=lambda:print("hi"))])


