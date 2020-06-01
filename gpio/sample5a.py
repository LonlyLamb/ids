"""
Laspberry Piのpullup抵抗設定と
スイッチの確認期待値
pullupの場合：スイッチを押すとLow
結果

配線
スイッチ両端を
GND：20pin
GPIO14：8pin
へ接続

リファクタリング：importされても実行されない
ように修正予定。
"""
"""
__author__ = "LonlyLamb<LonlyLamb@gmail.com>"
__status__ = "test"
__version__ = "0.0.1"
__date__    = "2020.05.24"

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
