import RPi.GPIO as GPIO
from time import sleep 

def perform(watering_pin,hor_pin,ver_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup((watering_pin,hor_pin,ver_pin),GPIO.OUT)
    GPIO.output((watering_pin,hor_pin,ver_pin),(GPIO.HIGH,GPIO.HIGH,GPIO.HIGH))
    sleep(2)
    GPIO.cleanup(watering_pin)
    hor_servo = GPIO.PWM(hor_pin,50)
    ver_servo = GPIO.PWM(ver_pin,50)
    hor_servo.ChangeDutyCycle(7.5)
    ver_servo.ChangeDutyCycle(7.5)
    sleep(0.5)
    GPIO.cleanup((hor_pin,ver_pin))
