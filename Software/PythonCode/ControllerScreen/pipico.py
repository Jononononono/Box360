print("hello world") #make sure that the pi is on
#first we import our packages
import board
import digitalio
from digitalio import *
from analogio import *
import gamepad
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

#now set all of the primary defenitions
kbd = Keyboard(usb_hid.devices) #how the keyboard is refered to
mouse = Mouse(usb_hid.devices) #same as the mouse
# now get the anologue stick controls
px = AnalogIn(board.GP26)
py = AnalogIn(board.GP27)
pc = DigitalInOut(board.GP6)
pc.switch_to_input(pull=Pull.UP)

#set up the HID keyboard controls
keycodes = [Keycode.UP_ARROW, Keycode.DOWN_ARROW]
pad = gamepad.GamePad(digitalio.DigitalInOut(board.GP12), digitalio.DigitalInOut(board.GP14))
last_pressed = 0

#all of the joystick options like sensitivity etc'
sensitivity = 5
midpoint = 32768
deadzone = 5000
invert = True
debug = True
#set all of the anologue get values function
def get_joystick_value(analog_input):
    value = analog_input.value - midpoint
    if abs(value) < deadzone:
        return 0
    return value / (midpoint - deadzone)


#main loop
while True:
    #pull values for everything
    this_pressed = pad.get_pressed()
    x = get_joystick_value(px)
    y = get_joystick_value(py)
    clk = not pc.value

    #mouse debug script for the moment
    if debug:
        print(f'px={px.value} | py={py.value} | x={x} | y={y} | clk={clk}')
    #if invert mode is on
    if invert:
        x = -x
        y = -y

    if clk: #click on the joystick
        mouse.click(Mouse.LEFT_BUTTON)

    #move the mouse
    move_x = int(x * sensitivity)
    move_y = int(y * sensitivity)
    if this_pressed != pad.get_pressed():
        if (this_pressed != last_pressed):
            for i in range(2):
                if (this_pressed & 1<<i) and not (last_pressed & 1<<i): #if a key is being pressed
                    kbd.press(keycodes[i]) #enable it
                if (last_pressed & 1<<i) and not (this_pressed & 1<<i): #else
                    kbd.release(keycodes[i]) #disable it

                last_pressed = this_pressed
            time.sleep(0.01)


