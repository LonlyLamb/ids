"""
侵入検知システム  Step3

__author__ = "H.Takeda"
__status__ = " test"
__version__ = "3.0.0.0"
__date__    = "2020.06.15"
"""

"""
s3ver2000.pyのクラスを関数に変更

SENSOR_PIN = 23  # センサーからの入力BCM指定
                 # BCM23=>pin16
センサー電圧5V pin4
LED_PIN = 18     # LEDへの出力BCM指定
                 # BCM18=>pin12

"""

import time
from datetime import datetime

# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO

INTERVAL = 10    # 計測間隔
BOUNCE =  1000   # 検出後の待機時間ms
LEDTIME = 2      # LED点灯時間
SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定

last_time = time.time()
cnt = 0
"""

"""


def init_gpio():
    global cnt
    global last_time
    # pythonは関数外で定義された変数を更新する場合、global宣言が必要

    cnt = 1
    last_time = time.time()

    # GPIO初期設定
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # SENSOR_PINを入力、プルダウンに設定
    GPIO.setup(SENSOR_PIN, GPIO.IN, GPIO.PUD_DOWN)
    # LED_PINを出力、初期値0に設定
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)


def set_event():
    # 割り込みイベント設定
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, bouncetime=BOUNCE)
    # コールバック関数登録
    GPIO.add_event_callback(SENSOR_PIN, my_callback_detect)


def my_callback_detect(SENSOR_PIN):
    global cnt
    global last_time

    def led(lpin):

        print("LED ON")
        GPIO.output(lpin,GPIO.HIGH)
        time.sleep(LEDTIME)
        GPIO.output(lpin,GPIO.LOW)
        print("LED OFF")


    if time.time() - last_time >= INTERVAL:
        """
        INTERVALによる制御はbouncetimeによる制御と重複しているが
        bouncetimeで指定できる時間の範囲がわからないのでINTERVAL
        指定を加えておく。
        """
        print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
        "：" + str("{0:05d}".format(cnt)) + "回目の人感知")

        led(LED_PIN)

        cnt += 1
        last_time = time.time()


def interval_proc():
    while True:
        print("sleep start")
        time.sleep(10)
        print("sleep end")



if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        init_gpio()
        set_event()
        interval_proc()
    except KeyboardInterrupt:
        print("終了処理中...")
        GPIO.remove_event_detect(SENSOR_PIN)
        GPIO.cleanup()
        print("GPIO clean完了")
# 終了処理
# KeyboardInterrupt側に持たせたので不要
"""
finally:
    GPIO.cleanup()
    print("finally GPIO clean完了")
"""
