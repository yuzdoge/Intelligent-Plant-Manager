import Myservant
import RPi.GPIO as GPIO
def main():
    Watering_PIN = 27
    Humiditydtc_PIN = 17
    hor_pin = 5
    ver_pin = 6
    Elia = Myservant.Servant(Watering_PIN,Humiditydtc_PIN,hor_pin,ver_pin)
    
    '''缺省进入mastermode'''
    while Elia.get_survival_status():
        if Elia.get_mode():
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            print('master mode')
            Elia.mastermode()
        
        if not Elia.get_mode():
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            print('lazy mode')
            Elia.lazymode()

if  __name__ == '__main__':
    main()
