import RPi.GPIO as GPIO
import time
"""
channelに接続したLEDを 2秒間隔で点滅させる。
LEDはBCM18(pin12)とGND(pin6)に接続する。
間に抵抗を入れること。

2020.05.26 リファクタリング：importされても実行されない
ように修正する。
"""

def led():
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

if __name__ == "__main__":
    led()
