import RPi.GPIO as GPIO
import time
"""
channelに接続したLEDを10秒間点灯させた後で終了する。
LEDはBCM18(pin12)とGND(pin6)に接続する。
間に抵抗を入れること。

2020.05.26 リファクタリング：importされても実行されない
ように修正する。
"""
def led():
    GPIO.setmode(GPIO.BCM)
    channel = 18
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(channel, GPIO.HIGH)
    # 10秒間点灯させるためsleepをいれる。
    time.sleep(10)
    GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    led()
