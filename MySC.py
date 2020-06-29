import RPi.GPIO as GPIO
import time 
import os 
import requests 
import json 
import urllib3.request 
import datetime 
import random 
import base64 
import numpy
import cv2
import watering

# onenet账号
url = 'http://api.heclouds.com/devices/590932977/datapoints'
API_KEY = "sBHLeW50Cy7DjOFpsrt=WSarjNE="
headers = {'api-key': API_KEY}


# 从onenet下载指令
def get_order():
    r = requests.get(url, headers=headers)
    text = r.text
    # print(text)
    jsonobj = json.loads(text)
    data = int(jsonobj['data']['datastreams'][0]['datapoints'][0]['value'])
    #print(data)
    control = int(data/10)
    flag = data%10
    return flag,control


def capture():
    #cap
    video_capture = cv2.VideoCapture(0)
    ret,pframe = video_capture.read()    

    #encode
    img_encode = cv2.imencode('.jpg',pframe)[1]
    s = base64.b64encode(img_encode)
    s = 'data:image/jpg;base64,'+ s.decode()

    #upload
    payload = {'datastreams': [{"id": "base", "datapoints": [{"value": s}]}]}
    jdata = json.dumps(payload)  # 对数据进行JSON格式化编码
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    print("上传成功")
    video_capture.release()


class Myservo():
    def __init__(self,hor_pin,ver_pin):
        self.hor_pin = hor_pin
        self.ver_pin = ver_pin

        self.hor_angle = 90
        self.ver_angle = 90                
        self.reset()
        
        self.usedflag, temp = get_order()
        print(self.usedflag,' ',temp)

    def get_servo(self,servo_pin):
        GPIO.setup(servo_pin,GPIO.OUT)
        servo = GPIO.PWM(servo_pin,50)
        servo.start(0)
        return servo       

    def set_horizontal(self,direction):
        hor_servo = self.get_servo(self.hor_pin)
        if direction == 4 and self.hor_angle<170: #向右
            self.hor_angle += 20 
        elif direction == 3 and self.hor_angle>10: #向左
            self.hor_angle -=20

        duty_cycles = self.hor_angle/18+2.5
        hor_servo.ChangeDutyCycle(duty_cycles)
        time.sleep(0.5)
        GPIO.cleanup(self.hor_pin)

    def set_vertical(self,direction):
        ver_servo = self.get_servo(self.ver_pin)
        if direction == 1 and self.ver_angle<180:
            self.ver_angle += 10
        elif direction == 2 and self.ver_angle>30:
            self.ver_angle -=10
        
        duty_cycles = self.ver_angle/18+2.5
        ver_servo.ChangeDutyCycle(duty_cycles)
        time.sleep(0.5)
        GPIO.cleanup(self.ver_pin)

    def reset(self):
        hor_servo = self.get_servo(self.hor_pin)
        ver_servo = self.get_servo(self.ver_pin)    
        hor_servo.ChangeDutyCycle(7.5)
        ver_servo.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        GPIO.cleanup((self.hor_pin,self.ver_pin))
                
    def isupdate(self,flag):
        if flag == self.usedflag:
            return False
        else:
            self.usedflag = flag
            return True


'''
hor_pin = 5
ver_pin = 6
s = Myservo(hor_pin,ver_pin)
q = 0
while True:
    flag,direction = get_order()
    time.sleep(0.5)
    
    if s.isupdate(flag):
        print(s.usedflag,' ',flag,' ',direction)
        if direction == 3 or direction == 4:
            s.set_horizontal(direction)
        if direction == 1 or direction == 2:
            s.set_vertical(direction)
        capture()
'''
