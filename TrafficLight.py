#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GreenLedPin = 11    # pin11 --- led
BtnPin = 12    # pin12 --- button
RedLedPin = 19 

Green_Led_status = 1
Red_Led_status = 1

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(GreenLedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.output(GreenLedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
	GPIO.setup(RedLedPin, GPIO.OUT)
	GPIO.output(RedLedPin, GPIO.HIGH)

def swGreenLed(ev=None):
	global Green_Led_status
	Green_Led_status = not Green_Led_status
	GPIO.output(GreenLedPin, Green_Led_status)  # switch led status(on-->off; off-->on)
	if Green_Led_status == 1:
		print('green led off...')
	else:
		print('...green led on')

def swRedLed(ev = None):
        global Red_Led_status
        Red_Led_status = not Red_Led_status
        GPIO.output(RedLedPin, Red_Led_status)
        if Red_Led_status == 1:
                print('red led off...')
        else:
                print('...red led on')

def crosswalk(ev = None):
        print('Crosswalk Button Pressed')
        swGreenLed()
        swRedLed()
        time.sleep(5)
        swRedLed()
        swGreenLed()

def loop():
	GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=crosswalk, bouncetime=500) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		time.sleep(1)   # Don't do anything

def destroy():
	GPIO.output(GreenLedPin, GPIO.HIGH)     # led off
	GPIO.output(RedLedPin, GPIO.HIGH)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	swGreenLed()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
