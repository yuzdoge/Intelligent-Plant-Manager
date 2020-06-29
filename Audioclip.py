import pygame
import os
import RPi.GPIO as GPIO
from time import sleep
from playsound import playsound

def play(IN_PIN,music):
    sleep(2)
    if GPIO.input(IN_PIN): #消抖动    
        print('start')
        music.pause()
        pos = pygame.mixer.music.get_pos()
        pos = pos/1000
        top_dir = os.path.dirname(os.path.abspath(__file__))
        address = os.path.join(top_dir,'resources/servant.mp3')
        pygame.mixer.music.load(address)

        while GPIO.input(IN_PIN):
            pygame.mixer.music.play()
            print('请浇水！')
            while pygame.mixer.music.get_busy():
                pass
     
        pygame.mixer.music.load(music.Music_list[music.music_num])
        pygame.mixer.music.play(start=pos)
