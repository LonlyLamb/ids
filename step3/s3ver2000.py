"""
侵入検知システム  Step3

__author__ = "H.Takeda"
__status__ = " test"
__version__ = "2.0.0.0"
__date__    = "2020.06.08"
"""

"""
s3ver2000.py <= クラス化バージョン、sample8_3.pyにインターバルタイム追加
sample8_3.py <= sample8_2.pyとs3ver1000.py
を統合

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
BOUNCE =  3000   # 検出後の待機時間ms
LEDTIME = 2      # LED点灯時間
SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定


class CallBack:

    def __init__(self):

        self.cnt = 1
        self.last_time = time.time()

        # GPIO初期設定
        #GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        # SENSOR_PINを入力、プルダウンに設定
        GPIO.setup(SENSOR_PIN, GPIO.IN, GPIO.PUD_DOWN)
        # LED_PINを出力、初期値0に設定
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

        # 割り込みイベント設定
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, bouncetime=BOUNCE)
        # コールバック関数登録
        GPIO.add_event_callback(SENSOR_PIN, self.my_callback_detect)


    def my_callback_detect(self, SENSOR_PIN):

        def led(lpin):
            """
            注）ledはクラスのメソッドではなく関数なので引数にselfは不要
            """
            print("LED ON")
            GPIO.output(lpin,GPIO.HIGH)
            time.sleep(LEDTIME)
            GPIO.output(lpin,GPIO.LOW)
            print("LED OFF")


        if time.time() - self.last_time >= INTERVAL:
            print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
            "：" + str("{0:05d}".format(self.cnt)) + "回目の人感知")

            led(LED_PIN)

            self.cnt += 1
            self.last_time = time.time()



if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        cb = CallBack()
        while True:
            print("sleep")
            time.sleep(10)
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
