import board
import digitalio
import displayio
import storage
import usb_cdc
import usb_midi

from time import sleep

b1 = digitalio.DigitalInOut(board.KEY1)
b1.switch_to_input(pull=digitalio.Pull.UP)

# Activate development mode if KEY1 is pressed
if not b1.value:
    print("Dev Mode: Active")
    usb_cdc.enable(console=True, data=True)
    sleep(5)
else:
    displayio.release_displays()
    usb_cdc.enable(console=False, data=True)
    storage.disable_usb_drive()

#usb_midi.disable()