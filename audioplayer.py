# Basic Python Music Player - using tkinter and pygame
# source: https://github.com/aglla/pyprojects/blob/master/music-player.py
# TODO: app class (maybe it'll fix dataframe and sampling problems)

from tkinter import *
import pygame
from scipy.io.wavfile import read
from pygame.sndarray import make_sound
from PIL import Image, ImageTk
import pandas as pd
import numpy as np


def play(event=None):
    pygame.mixer.music.stop()
    sound = make_sound(mix)

    pygame.mixer.Sound(sound).play()


def prepare_mix():
    random_picks = db[['id', 'path']].loc[(db['sex'] == np.random.choice(['f', 'm'], 1)[0]) &
                                          (db['mod'] == 'n')].sample(n=2)
    if random_picks.values[0][0] == random_picks.values[1][0]:
        same_speaker = True
    else:
        same_speaker = False

    _, sig1 = read(corename + '\\' + random_picks.values[0][1])
    _, sig2 = read(corename + '\\' + random_picks.values[1][1])

    mix = np.concatenate((sig1, np.zeros(int(0.5 * rate), dtype='int16'), sig2))
    mix += np.random.randint(-2 ** 13, 2 ** 13, size=mix.shape, dtype='int16')

    return mix, same_speaker, random_picks


def same(event=None):
    log_record(True == same_speaker)


def different(event=None):
    log_record(False == same_speaker)


def log_record(ans):
    record = {"play_count": 1,
              "same_speaker": same_speaker,
              "sig1_name": random_picks.values[0][1],
              "sig2_name": random_picks.values[1][1],
              "SNR": 0,
              "correct": ans,
              "turning_points": 0}
    log.append(record, ignore_index=True)
    print(log)


db = pd.read_csv('D:\\phd\\phdDB_test.csv', sep=',', index_col=0)
corename = 'D:\\phd\\DATA'
rate = 44100
log = pd.DataFrame(columns=["play_count", "same_speaker", "sig1_name", "sig2_name",
                           "SNR", "correct", "turning_points"])

mix, same_speaker, random_picks = prepare_mix()

root = Tk()
root.title('19/EXP01')
root.config(bg='#002d69')

baseh = 150

v = Image.open('.\\img\\uam_full.jpg')
v = v.resize((int((float(v.size[0])*(baseh/float(v.size[1])))), baseh), Image.ANTIALIAS)
logoU = ImageTk.PhotoImage(v)
logoUAM = Label(image=logoU)

manual = Label(root, text='Kliknij przycisk ⏯, aby odtworzyć nagranie. Usłyszysz dwie następujące po sobie '
                          'wypowiedzi. \n\n Określ proszę, klikając odpowiedni przycisk, czy wypowiedzi te '
                          'pochodzą od tego samego, czy od różnych mówców.',
               fg='#ffffff',
               bg='#002d69',
               font=('Calibri', 12),
               padx=20,
               pady=20,
               wraplength=300)
playButton = Button(root, text='⏯', font=('Calibri', 36), bg='#ffffff', command=play)
firstAns = Button(root, text='Ta sama osoba', bg='#ffffff', font=('Calibri', 14), width=20, height=5, command=same)
secondAns = Button(root, text='Różne osoby', bg='#ffffff', font=('Calibri', 14), width=20, height=5, command=different)

modx, mody = 30, 20
logoUAM.grid(row=0, column=0)
manual.grid(row=0, column=1)
playButton.grid(row=2, column=0, padx=modx, pady=mody)
firstAns.grid(row=1, column=1, padx=modx, pady=mody)
secondAns.grid(row=3, column=1, padx=modx, pady=mody)

pygame.mixer.pre_init(frequency=rate, channels=1)
pygame.mixer.init()

# key bindings
root.bind('s', same)
root.bind('d', different)
root.bind('<space>', play)

mainloop()
