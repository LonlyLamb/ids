import RPi.GPIO as GPIO
import time

"""
超音波距離センサーテストプログラム
file name: sample6_2.py
超音波距離センサー: HC-SR04
センサーの端子: Vcc,Trig,Echo,Gnd
Vcc: 5V  2(pin)
TRIG_PIN = 14(BCM)  8(pin)
ECHO_PIN = 15(BCM)  10(pin)
但し、Echo電圧5Vを10KΩと5.1KΩで3.3Vに減圧してRasPiに接続する。
Gnd: 14(pin)
"""
__author__ = "LonlyLamb@gmail.com"
__status__ = "test"
__version__ = "1.0.0"
__date__    = "2020.06.12"


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
    # ピン設定解除
    GPIO.cleanup()

#音速計算
def calc_sonic_velocity(t):
    return (331.50 + 0.61 * t) * 100


if __name__ == "__main__":

    # TRIGとECHOのGPIO番号
    TRIG_PIN = 14
    ECHO_PIN = 15

    TEMPERATURE = 25

    # ピン番号をGPIOで指定
    GPIO.setmode(GPIO.BCM)
    # TRIG_PINを出力, ECHO_PINを入力
    GPIO.setup(TRIG_PIN,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(ECHO_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setwarnings(False)

    # 気温から音速計算
    sv = calc_sonic_velocity(TEMPERATURE)

    # 距離計測(TRIGピン番号, ECHO_PIN番号, 計測回数, 音速[cm/s])
    calc_distance(TRIG_PIN, ECHO_PIN, 10, sv)
