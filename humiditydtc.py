from gpiozero import DigitalInputDevice as DID
from time import sleep

PIN = 17
IN_PIN = DID(pin=17,pull_up=None,active_state=True,bounce_time=0.05)

def watering(IN_PIN):
    #该参数是产生中断的设备(端口)
    while IN_PIN.value:
        print('正在浇水...')
        sleep(5)

IN_PIN.when_activated = watering
while True:
    print(IN_PIN.value)
    sleep(1)



