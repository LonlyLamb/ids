# -*- coding: utf-8 -*-
"""
侵入検知システム  Step3
"""
__author__ = "H.Takeda"
__status__ = " test"
__version__ = "1.0.0.0"
__date__    = "2020.04.29"


from datetime import datetime
import time
# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO


INTERVAL = 2     # 計測間隔
SLEEPTIME = 10   # 検出後の待機時間
SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定

# GPIOの初期設定
GPIO.cleanup()  #念のためcleanup()を追加
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

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
        GPIO.cleanup()  #注 finallyは例外が発生した場合もしなかった場合
                        #も常に最後に行う処理なので、except中に記述不要。
        print("GPIO clean完了")
