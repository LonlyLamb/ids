import RPi.GPIO as GPIO
"""
配線
GPIO4：7pin
と
GND:9pin
を開放しておく。接続してエッジを発生させる。

2020.06.04 終了処理を追加した。
しかし、timeout=5000としてあるとKeyboardInterrupt時の処理が
走るまでに5秒かかることもある。
"""

class CallBack:

    def __init__(self):
        # 4番pinを入力、プルアップに設定
        self.pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP)

    def callback_test(self):

        while(True):
            # 立下りエッジイベント、タイムアウトイベント待ち
            isr = GPIO.wait_for_edge(self.pin, GPIO.FALLING, timeout=5000,  bouncetime=1000)
            if isr is None:
                # 5秒間割り込みがないときに実行される
                print("5秒間割り込みなし")
            else:
                # 割り込みがあったときに実行される
                print("割り込みあり")

try:
    print("プログラム　スタート")
    cb = CallBack()
    cb.callback_test()
except KeyboardInterrupt:
    print("終了処理中...")
    GPIO.cleanup()
    print("GPIO clean完了")
