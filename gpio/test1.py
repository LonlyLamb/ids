"""
https://www.denshi.club/pc/python/iotpython3l.html
"""
import RPi.GPIO as GPIO
import time
sw1 = 20
sw2 = 16

def my_callback1(sw1):
    print('\n at GPIO20')

def my_callback2(sw2):
    print('\n at GPIO16')

GPIO.setmode(GPIO.BCM)
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(sw1, GPIO.RISING, callback=my_callback1, bouncetime=200)
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(sw2, GPIO.RISING, callback=my_callback2, bouncetime=200)

try:
    while 1:
        print('\n Press any key to exit.\n')
        time.sleep(1)
except KeyboardInterrupt:
    print('\n end')
    GPIO.cleanup()
