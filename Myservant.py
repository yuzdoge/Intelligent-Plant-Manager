import snowboydecoder
import BaiduSdk
import Pymusic
import vadSound
import os
import wateringx
import Audioclip
#from gpiozero import DigitalInputDevice as DID
import RPi.GPIO as GPIO
from time import sleep
from multiprocessing import Process,Event
import MySC
import pygame

class Servant:
    def __init__(self,Watering_PIN,Humiditydtc_PIN,hor_pin,ver_pin):
        self.Watering_PIN = Watering_PIN
        self.Humiditydtc_PIN = Humiditydtc_PIN
        self.hor_pin = hor_pin
        self.ver_pin = ver_pin
        self.__music = Pymusic.Music()
        self.__result = None
        self.__mode = True #True:mastermode,False:lazymode
        self.__survival = True
        self.__interrupted = False
    
    def mastermode(self):
        self.__interrupted = False
        #IN_PIN = DID(pin=self.Humiditydtc_PIN,pull_up=None,active_state=True,bounce_time=0.05)
        #IN_PIN.when_activated = lambda:Audioclip.play(IN_PIN,self.__music) 
        GPIO.setup(self.Humiditydtc_PIN,GPIO.IN)
        GPIO.add_event_detect(self.Humiditydtc_PIN,GPIO.RISING,callback=self.humidity_callback,bouncetime=200)
        #GPIO.add_event_callback(self.Humiditydtc_PIN,lambda:Audioclip.play(self.__music),bouncetime=200)

        top_dir = os.path.dirname(os.path.abspath(__file__))
        keyword = os.path.join(top_dir,'resources/models/snowboy.umdl')

        detector = snowboydecoder.HotwordDetector(keyword, sensitivity=0.5)
        detector.start(detected_callback = self.master_listen,interrupt_check=self.interrupt_callback)
        #IN_PIN.close()
        detector.terminate()

    def lazymode(self):
        self.__interrupted = False
        
        loop = Event()
        loop.set()
        subprocess = Process(target=lazy_function,args=(loop,self.Watering_PIN,self.Humiditydtc_PIN,self.hor_pin,self.ver_pin))
        subprocess.start()
        
        top_dir = os.path.dirname(os.path.abspath(__file__))
        keyword = os.path.join(top_dir,'resources/models/snowboy.umdl')
        
        detector = snowboydecoder.HotwordDetector(keyword, sensitivity=0.5)
        detector.start(detected_callback = self.lazy_listen,interrupt_check=self.interrupt_callback)
        detector.terminate()
        
        loop.clear()
        subprocess.join()
        subprocess.terminate()
                
    def listen(self):
        snowboydecoder.play_audio_file() #播放提示音
        print('listen...')
        vadSound.record_sound()
        Flag,self.__result = BaiduSdk.sound2text()
        print(self.__result)
    
    def master_listen(self):
        self.listen()
        try:
            self.behavior_check()
        except:
            pass        

    def lazy_listen(self):
        self.listen()
        if '主人' in self.__result:
            self.__mode = True
            self.__interrupted = True
            GPIO.cleanup()

        elif '关机' in self.__result:
            self.__interrupted = True
            self.__survival = False
            GPIO.cleanup()

    def behavior_check(self):
        if '浇' in self.__result or '水' in self.__result or '花' in self.__result:
            wateringx.perform(self.Watering_PIN,self.hor_pin,self.ver_pin)

        elif '播放' in self.__result and not '继续' in self.__result :
            self.__music.play()

        elif '停' in self.__result:
            self.__music.pause()

        elif '继续' in self.__result:
            self.__music.unpause()

        elif '关闭' in self.__result:
            self.__music.stop()

        elif '上一首' in self.__result:
            self.__music.previous()

        elif '下一首' in self.__result:
            self.__music.nextsong()

        elif '大声' in self.__result and not '最' in self.__result:
            self.__music.turnup()

        elif '小声' in self.__result:
            self.__music.turndown()
        
        elif '最大声' in self.__result:
            self.__music.volume = 0.9
            self.__music.turnup()
        
        elif '静音' in self.__result:
            self.__music.volume = 0.1
            self.__music.turndown() 

        elif '懒人' in self.__result:
            self.__music.stop()
            self.__mode = False
            self.__interrupted = True
            GPIO.cleanup()

        elif '关机' in self.__result:
            self.__music.stop()
            self.__interrupted = True
            self.__survival = False
            GPIO.cleanup()        

    def get_survival_status(self):
        return self.__survival

    def get_mode(self):
        return self.__mode

    def interrupt_callback(self):
        return self.__interrupted

    def humidity_callback(self,PIN):
        return Audioclip.play(self.Humiditydtc_PIN,self.__music)
      

def lazy_function(loop,Watering_PIN,Humiditydtc_PIN,hor_pin,ver_pin):
    #IN_PIN = DID(pin=Humiditydtc_PIN,pull_up=None,active_state=True,bounce_time=0.05)
    GPIO.setup(Humiditydtc_PIN,GPIO.IN)
    s = MySC.Myservo(hor_pin,ver_pin)
    while loop.is_set():
        #if IN_PIN.value:
        if GPIO.input(Humiditydtc_PIN):
            wateringx.perform(Watering_PIN,hor_pin,ver_pin)
            #print('浇水...')
            #sleep(5)
      
        flag,direction = MySC.get_order()
        sleep(0.5)
        if s.isupdate(flag):
            print(s.usedflag,' ',flag,' ',direction)
            if direction == 3 or direction == 4:
                s.set_horizontal(direction)
            if direction == 1 or direction == 2:
                s.set_vertical(direction)
            MySC.capture()

    #IN_PIN.close()
    #s.close()

