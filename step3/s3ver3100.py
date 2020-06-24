"""
侵入検知システム  Step3

__author__ = "H.Takeda"
__status__ = " test"
__version__ = "3.0.0.0"
__date__    = "2020.06.15"
"""

"""
s3ver3000.pyに超音波距離センサーを追加

赤外線センサー
SENSOR_PIN = 23  # センサーからの入力BCM指定
                 # BCM23=>pin16
センサー電圧5V pin4
LED_PIN = 18     # LEDへの出力BCM指定
                 # BCM18=>pin12

超音波距離センサー
超音波距離センサー: HC-SR04
センサーの端子: Vcc,Trig,Echo,Gnd
Vcc: 5V  2(pin)
TRIG_PIN = 14(BCM)  8(pin)
ECHO_PIN = 15(BCM)  10(pin)
但し、Echo電圧5Vを10KΩと5.1KΩで3.3Vに減圧してRasPiに接続する。
Gnd: 14(pin)

"""

import time
from datetime import datetime

# GPIO制御ライブラリはRPi.GPIOを用いる。
import RPi.GPIO as GPIO

#赤外線センサー
INTERVAL = 10    # 計測間隔
BOUNCE =  1000   # 検出後の待機時間ms
LEDTIME = 2      # LED点灯時間
SENSOR_PIN = 23  # センサーからの入力BCM指定
LED_PIN = 18     # LEDへの出力BCM指定

#超音波距離センサー
TRIG_PIN = 14
ECHO_PIN = 15

TEMPERATURE = 25   #当面気温は固定としておく


INIT_DISTANCE = 300

last_time = time.time()
cnt = 0


#音速計算
def calc_sonic_velocity(t):
    return (331.50 + 0.61 * t) * 100

# HIGH or LOWの時計測
def pulseIn(PIN, start=1, end=0):
    if start==0: end = 1
    t_start = 0
    t_end = 0

    # ECHO_PINがHIGHである時間を計測
    # ECHO_PINがHIGHになる時刻
    while GPIO.input(PIN) == end:
        t_start = time.time()
    # ECHO_PINのHIGHが終了する時刻
    while GPIO.input(PIN) == start:
        t_end = time.time()
    return t_end - t_start


# 距離計測
def calc_distance(TRIG_PIN, ECHO_PIN, num, v):
    sum_d = 0
    for i in range(num):
        # TRIGピンを0.3[s]だけLOW
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.3)
        # TRIGピンを0.00001[s]だけ出力(超音波発射)
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        # HIGHの時間計測
        t = pulseIn(ECHO_PIN)
        # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = v * t/2
        sum_d += distance
        print(i,":",distance, "cm")
    print("average distance = ",sum_d/num, "cm")
    return sum_d/num
    # ピン設定解除
    #GPIO.cleanup()


def init_gpio():
    global cnt
    global last_time
    global INIT_DISTANCE

    cnt = 1
    last_time = time.time()

    # GPIO初期設定
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # SENSOR_PINを入力、プルダウンに設定
    GPIO.setup(SENSOR_PIN, GPIO.IN, GPIO.PUD_DOWN)
    # LED_PINを出力、初期値0に設定
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    # TRIG_PINを出力, ECHO_PINを入力
    GPIO.setup(TRIG_PIN,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(ECHO_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    # 気温から音速計算
    sv = calc_sonic_velocity(TEMPERATURE)
    INIT_DISTANCE = calc_distance(TRIG_PIN, ECHO_PIN, 5, sv)


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
        sv = calc_sonic_velocity(TEMPERATURE)
        if calc_distance(TRIG_PIN, ECHO_PIN, 5, sv) < INIT_DISTANCE * 0.9:

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
