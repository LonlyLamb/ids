import RPi.GPIO as GPIO
import time
"""
channelに接続したLEDを 2秒間隔で点滅させる。　
"""
GPIO.setmode(GPIO.BCM)
channel = 18
GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
print("終了はCtrl+C")
try:
    while True:
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(2)
except KeyboardInterrupt:
    print("終了します")
    GPIO.cleanup()
