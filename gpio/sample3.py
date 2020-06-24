import RPi.GPIO as GPIO
import time
"""
channelに接続したLEDの明るさを変更する（擬似的アナログ出力）。

"""

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    channel = 18
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    print("終了はCtrl+C")

    led = GPIO.PWM(channel, 100)    # LED1の周波数設定(100Hz)
    led.start(0)                    # デューティ比 0 でPWM出力開始

    try:
        while True:
            # 0〜100まで10段階でデューティ比を設定(プラス方向)
            for dc in range(0,100,10):
                led.ChangeDutyCycle(dc)
                time.sleep(0.5)
            # 100〜0まで10段階でデューティ比を設定(マイナス方向)
            for dc in range(100,0,-10):
                led.ChangeDutyCycle(dc)
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("終了します")
        led.stop()      # PWM出力を停止
        GPIO.cleanup()
