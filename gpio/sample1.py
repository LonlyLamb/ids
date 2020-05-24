import RPi.GPIO as GPIO
import time
"""
channelに接続したLEDを10秒間点灯させた後で終了する。　
"""
GPIO.setmode(GPIO.BCM)
channel = 18
GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(channel, GPIO.HIGH)
time.sleep(10)
GPIO.output(channel, GPIO.LOW)
GPIO.cleanup()
