# -*- coding: utf-8 -*-
"""
侵入検知システム  Step4
"""
__author__ = "H.Takeda"
__status__ = " test"
__version__ = "1.0.0.0"
__date__    = "2020.04.29"

from datetime import datetime
import time
# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO
from pushbullet import Pushbullet


INTERVAL = 5     # 計測間隔
SLEEPTIME = 10   # 検出後の待機時間

SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定

# PushbulletのAPIキー設定
apikey = "o.gpJ6P67e17nBH90711BrCiU1LcR9DUbZ"
pb = Pushbullet(apikey)


GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        cnt = 1

        while True:
            # センサー検出時
            if(GPIO.input(SENSOR_PIN) == GPIO.HIGH):
                print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                "：" + str("{0:05d}".format(cnt)) + "回目の人感知")
                cnt = cnt + 1
                GPIO.output(LED_PIN,GPIO.HIGH)
                # 頻繁なushbulletへの通知はさける
                #push = pb.push_note("RaspberryPi", "人の動きを検知しました")
                push =  pb.push_note("RaspberryPi", datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                "：" + str("{0:05d}".format(cnt)) + "回目の人感知") 
                time.sleep(SLEEPTIME)
                GPIO.output(LED_PIN,GPIO.LOW)
            # センサー未検出時
            else:
                print(GPIO.input(SENSOR_PIN))
                time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("終了処理中...")
    # 終了処理
    finally:
        GPIO.cleanup()
        print("GPIO clean完了")
