# Basic Python Music Player - using tkinter and pygame
# source: https://github.com/aglla/pyprojects/blob/master/music-player.py

from tkinter import *
import pygame
from scipy.io.wavfile import read
from pygame.sndarray import make_sound
from PIL import Image, ImageTk


def play():
    pygame.mixer.music.stop()
    rate, signal = read('D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_001.wav')
    sound = make_sound(signal)

    pygame.mixer.Sound(sound).play()


root = Tk()
root.title('19/EXP01')
root.config(bg="#002d69")

baseh = 100

v = Image.open('.\\img\\uam_full.jpg')
v = v.resize((int((float(v.size[0])*(baseh/float(v.size[1])))), 100), Image.ANTIALIAS)
logoU = ImageTk.PhotoImage(v)
logoUAM = Label(image=logoU)

playButton = Button(root, text='Odtwórz', command=play)
firstAns = Button(root, text='Ta sama osoba')
secondAns = Button(root, text='Różne osoby')

modx, mody = 50, 50

logoUAM.grid(row=0, column=0)
playButton.grid(row=2, column=0, padx=modx, pady=mody)
firstAns.grid(row=1, column=1, padx=modx, pady=mody)
secondAns.grid(row=3, column=1, padx=modx, pady=mody)
        # self.playButton.place(x=0, y=0)
# root.pack()

pygame.mixer.pre_init(frequency=44100, channels=1)
pygame.mixer.init()


mainloop()
