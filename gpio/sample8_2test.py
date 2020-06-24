import RPi.GPIO as GPIO
import time
import logging
import threading

PIN = 4
"""
配線
GPIO4：7pin
と
GND:9pin
を開放しておく。接続してエッジを発生させる。

"""

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)

def set_event():
    # 割り込みイベント設定
    GPIO.add_event_detect(PIN, GPIO.RISING, bouncetime=1000)
    # コールバック関数登録
    GPIO.add_event_callback(PIN, my_callback_one)
    GPIO.add_event_callback(PIN, my_callback_two)

def interval_proc():
    while True:
        print("sleep start")
        time.sleep(10)
        print("sleep end")



def my_callback_one(PIN):
    print('Callback one')
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

def my_callback_two(PIN):
    print('Callback two')
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')



if __name__ == '__main__':
    try:
        logging.debug('START')
        init_gpio()
        set_event()
        interval_proc()

    except KeyboardInterrupt:
        print("終了処理中...")
        GPIO.remove_event_detect(PIN)
        GPIO.cleanup()
        print("GPIO clean完了")
        logging.debug('END')
