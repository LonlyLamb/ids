"""
sample8_3.py
sample8_2.pyとs3ver1000.py
を統合

SENSOR_PIN = 23  # センサーからの入力BCM指定
                 # BCM23=>pin16
センサー電圧5V pin4
LED_PIN = 18     # LEDへの出力BCM指定
                 # BCM18=>pin12
"""
import RPi.GPIO as GPIO
import time

from datetime import datetime
import time
# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO


#INTERVAL = 3     # 計測間隔
SLEEPTIME = 3000   # 検出後の待機時間ms
LEDTIME = 2      # LED点灯時間
SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定
"""

"""

class CallBack:

    def __init__(self):


        GPIO.setmode(GPIO.BCM)
        # SENSOR_PINを入力、プルダウンに設定
        GPIO.setup(SENSOR_PIN, GPIO.IN, GPIO.PUD_DOWN)
        # LED_PINを出力、初期値0に設定
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

        # 割り込みイベント設定
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, bouncetime=SLEEPTIME)
        # コールバック関数登録
        GPIO.add_event_callback(SENSOR_PIN, self.my_callback_print)
        GPIO.add_event_callback(SENSOR_PIN, self.my_callback_led)

        cnt = 1

    def my_callback_print(self, SENSOR_PIN):
        print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
        "：" + str("{0:05d}".format(cnt)) + "回目の人感知")
        cnt = cnt + 1

    def my_callback_led(self, SENSOR_PIN):
        GPIO.output(LED_PIN,GPIO.HIGH)
        time.sleep(LEDTIME)
        GPIO.output(LED_PIN,GPIO.LOW)


if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        cb = CallBack()
    except KeybordInterrupt:
        print("終了処理中...")
    # 終了処理
    finally:
        GPIO.cleanup()
        print("GPIO clean完了")
