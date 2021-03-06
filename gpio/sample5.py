"""
Laspberry Piのpulldown抵抗設定と
スイッチの確認

期待値
pulldownの場合：スイッチを押すとHigh
結果
OK

配線
スイッチ両端を
3.3V：1pin
GPIO14：8pin
へ接続
"""
__author__ = "LonlyLamb<LonlyLamb@gmail.com>"
__status__ = "test"
__version__ = "0.0.1"
__date__    = "2020.05.24"

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == "__main__":
    try:
        while True:
            if GPIO.input(14) == GPIO.HIGH:
                print("14High")
            else:
                print("14Low")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Ctrl+Cで停止します")
        pass

    GPIO.cleanup()
    print("cleanup end")
