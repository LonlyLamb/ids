import RPi.GPIO as GPIO
import time
"""
配線
GPIO4：7pin
と
GND:9pin
を開放しておく。接続してエッジを発生させる。

終了処理を追加すること。
"""

class CallBack:

    def __init__(self):

        # 4番pinを入力、プルアップに設定
        pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

        # 割り込みイベント設定
        GPIO.add_event_detect(pin, GPIO.RISING, bouncetime=1000)
        # コールバック関数登録
        GPIO.add_event_callback(pin, self.my_callback_one)
        GPIO.add_event_callback(pin, self.my_callback_two)

    def my_callback_one(self, channel):
        print('Callback one')

    def my_callback_two(self, channel):
        print('Callback two')

    def callback_test(self):
        print("call_back test start")
        while True:
            print("call_back test sleep start")
            time.sleep(1)
            print("call_back test sleep end")

cb = CallBack()
#cb.callback_test() # 割り込みイベント待ち
