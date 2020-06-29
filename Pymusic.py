import pygame
import threading
import os
from time import sleep


class Music_List():
    def __init__(self):
        # 播放列表
        self.play_list = []
        # 默认文件夹
        top_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_dir = os.path.join(top_dir,"music")
    def get_play_list(self):
        # 开始遍历目录
        #os.walk(top=adress,topdown=True,onerror=回调函数,followinks=False)；top必选，根目录；
        #os.walk方法放回一个迭代器，迭代器每一个元素是一个三元组(root,dirs,files)；root是当前目录的地址(字符串)，dirs是该目录下子目录的名称 列表，files是改目录下文件的名称 列表
        for root, dirs, files in os.walk(self.file_dir): 
            for file in files:
                if '.mp3' in file:
                    self.play_list.append(self.file_dir + "/" + file)
        print(self.play_list)
        return self.play_list

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.__playflag = False #用于控制子线程的进行
        self.__pauseflag = False

        self.__playthread = None #播放线程，如果用进程比较麻烦，数据不好交互
        #self.lock = threading.Lock() #用于解决上/下切换歌曲与子线程的冲突
        
        self.music_num = 0
        self.volume = 0.1
        self.Music_list = Music_List().get_play_list() #获取音乐列表
        self.__listlength = len(self.Music_list)
        
        self.load_music(self.Music_list[self.music_num]) #加载第一首
        pygame.mixer.music.set_volume(self.volume) #初始化音量
    
    '''function'''
    def initialize(self):
        self.__playflag = False
        self.__pauseflag = False
        self.__playthread = None
        self.music_num = 0
        self.volume = 0.1
        self.load_music(self.Music_list[self.music_num])
        pygame.mixer.music.set_volume(self.volume)

    def load_music(self,titlt):#加载音乐
        try:
            pygame.mixer.music.load(titlt)#载入一个音频流，相当于把数据给准备好，如果该音频流已经在播放，则该函数会中断该音频刘
        except :
            pass

    def play(self):
        if not self.__playflag:
            self.__playflag = True
            self.__pauseflag = False
            pygame.mixer.music.play()
            self.__playthread = threading.Thread(target=listloop,args=(self,))
            self.__playthread.start()
    
    def pause(self):
        self.__pauseflag = True
        pygame.mixer.music.pause()
    
    def unpause(self):
        self.__pauseflag = False
        pygame.mixer.music.unpause()
     
    def nextsong(self):
        if self.__playflag:
            self.__pauseflag = True #解决上/下切换歌曲与子线程的冲突
            self.music_num = (self.music_num+1) % self.__listlength
            self.load_music(self.Music_list[self.music_num])
            pygame.mixer.music.play()
            self.__pauseflag = False

    def previous(self):
        if self.__playflag:
            self.__pauseflag = True
            self.music_num = (self.music_num-1) % self.__listlength
            self.load_music(self.Music_list[self.music_num])
            pygame.mixer.music.play()
            self.__pauseflag = False

    def turnup(self):
        if self.__playflag:
            self.volume +=0.1
            pygame.mixer.music.set_volume(self.volume)#设置音乐播放的音量。值参数在0.0和1.0之间。当加载新音乐时，音量就会重置。
            print("音量："+str(100*self.volume))

    def turndown(self):
        if self.__playflag:
            self.volume -=0.1
            pygame.mixer.music.set_volume(self.volume)
            print("音量："+str(100*self.volume))

    def stop(self):
        self.initialize()
        pygame.mixer.music.fadeout(3)

    '''flag'''
    def isbusy(self):
        return pygame.mixer_music.get_busy()
    
    def get_playflag(self):
        return self.__playflag
    
    def get_pauseflag(self):
        return self.__pauseflag


def listloop(music):
    while music.get_playflag():
        if (not music.isbusy()) and (not music.get_pauseflag()): #当前音乐已经播放完毕
            #print('hhh')
            music.nextsong()
    
