# -*- coding: utf-8 -*-
"""
侵入検知システム  Step4
rev_a:pushbullet間隔を取る仕組みを追加
"""
__author__ = "H.Takeda"
__status__ = " test"
__version__ = "1.0.0.1"
__date__    = "2020.05.03"

from datetime import datetime
import time
# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO
from pushbullet import Pushbullet


INTERVAL = 3     # 計測間隔
SLEEPTIME = 7   # 検出後の待機時間
PUSH_INTERVAL =  180 # pushbullet通知の待機時間

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
        last_push_time =  time.time()

        while True:
            # センサー検出時
            if(GPIO.input(SENSOR_PIN) == GPIO.HIGH):
                print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                "：" + str("{0:05d}".format(cnt)) + "回目の人感知")
                cnt = cnt + 1
                GPIO.output(LED_PIN,GPIO.HIGH)
                # 頻繁なushbulletへの通知はさける
                # PUSH_INTERVAL間は再通知しないように変更した rev_a
                ss = time.time() - last_push_time
                print(ss)

                if ss > PUSH_INTERVAL:
                    #push = pb.push_note("RaspberryPi", "人の動きを検知しました")
                    push =  pb.push_note("RaspberryPi", datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                    "：" + str("{0:05d}".format(cnt)) + "回目の人感知")
                    last_push_time = time.time()

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
