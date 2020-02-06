# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Basic Python Music Player - using tkinter and pygame
based on: https://github.com/aglla/pyprojects/blob/master/music-player.py
TODO: welcome window with a simple survey and a short experiment info
'''

from tkinter import *
from tkinter import messagebox
import pygame
from scipy.io.wavfile import read
from pygame.sndarray import make_sound
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import os
from utils import rms


class App(Frame):

    def __init__(self, master):
        super(App, self).__init__(master)

        # TEST SETTINGS, CHANGE BEFORE RUN
        self.db = pd.read_csv('D:\\phd\\phdDB_test.csv', sep=',', index_col=0)
        # self.db = pd.read_csv('E:\\PhD\\recDataAn\\phdDB_test.csv', sep=',', index_col=0)
        self.stop_after = 2
        self.verbose = True
        # END OF TEST SETTINGS

        self.corename = 'D:\\phd\\DATA'
        # self.corename = 'E:\\PhD\\recDataAn'
        self.rate = 44100
        self.play_count = 0
        self.turning_points = 0
        self.target_SNR = 6
        _, self.babble = read('babble.wav')
        self.step = 3
        self.log = pd.DataFrame(columns=["play_count", "same_speaker", "sig1_name", "sig2_name",
                                         "SNR", "correct", "turning_points"])

        self.config(bg='#002d69')
        self.grid(rowspan=5, columnspan=2)

        baseh = 150
        v = Image.open('.\\img\\uam_full.jpg')
        v = v.resize((int((float(v.size[0])*(baseh/float(v.size[1])))), baseh), Image.ANTIALIAS)
        self.logoU = ImageTk.PhotoImage(v)
        self.logoUAM = Label(self, image=self.logoU)

        self.manual = Label(self,
                            text='Kliknij przycisk ⏯, aby odtworzyć nagranie. Usłyszysz dwie następujące po sobie '
                                  'wypowiedzi. \n\n Określ proszę, klikając odpowiedni przycisk, czy wypowiedzi te '
                                  'pochodzą od tego samego, czy od różnych mówców.',
                            fg='#ffffff',
                            bg='#002d69',
                            font=('Calibri', 12),
                            padx=20, pady=20,
                            wraplength=300)

        self.playButton = Button(self,
                                 text='⏯',
                                 font=('Calibri', 36),
                                 bg='#ffffff',
                                 command=self.play)

        self.firstAns = Button(self,
                               text='Ta sama osoba [s]',
                               bg='#ffffff',
                               font=('Calibri', 14),
                               width=20, height=5,
                               command=self.same)

        self.secondAns = Button(self,
                                text='Różne osoby [d]',
                                bg='#ffffff',
                                font=('Calibri', 14),
                                width=20, height=5,
                                command=self.different)

        modx, mody = 30, 20
        self.logoUAM.grid(row=0, column=0)
        self.manual.grid(row=0, column=1)
        self.playButton.grid(row=2, column=0, padx=modx, pady=mody)
        self.firstAns.grid(row=1, column=1, padx=modx, pady=mody)
        self.secondAns.grid(row=3, column=1, padx=modx, pady=mody)

        pygame.mixer.pre_init(frequency=self.rate, channels=1)
        pygame.mixer.init()

        self.mix, self.same_speaker, self.random_picks = None, None, None
        self.prepare_mix()

    def play(self, event=None):
        self.play_count += 1
        pygame.mixer.music.stop()
        sound = make_sound(self.mix)

        pygame.mixer.Sound(sound).play()

    def prepare_mix(self):
        self.random_picks = self.db[['id', 'path']].loc[(self.db['sex'] == np.random.choice(['f', 'm'], 1)[0]) &
                                                        (self.db['mod'] == 'n')].sample(n=2)
        if self.random_picks.values[0][0] == self.random_picks.values[1][0]:
            self.same_speaker = True
        else:
            self.same_speaker = False

        _, sig1_int = read(self.corename + '\\' + self.random_picks.values[0][1])
        _, sig2_int = read(self.corename + '\\' + self.random_picks.values[1][1])

        sig1 = sig1_int / 2**15
        sig2 = sig2_int / 2**15

        noise = self.babble[:len(sig1) + int(0.5 * self.rate) + len(sig2)] / 2**15

        sig1 *= (rms(noise) * 10 ** (self.target_SNR / 20)) / rms(sig1)
        sig2 *= (rms(noise) * 10 ** (self.target_SNR / 20)) / rms(sig2)

        self.mix = np.concatenate((sig1, np.zeros(int(0.5 * self.rate), dtype='float32'), sig2))
        self.mix += noise
        self.mix *= 2**15
        self.mix = self.mix.astype(dtype='int16')

    def same(self, event=None):
        self.log_record(self.same_speaker == True)

    def different(self, event=None):
        self.log_record(self.same_speaker == False)

    def log_record(self, ans):

        if not self.log.empty:
            if self.log['correct'].values[-1] != ans:
                self.turning_points += 1

        self.log = self.log.append({"play_count": self.play_count,
                                    "same_speaker": self.same_speaker,
                                    "sig1_name": self.random_picks.values[0][1].split(sep='\\')[-1],
                                    "sig2_name": self.random_picks.values[1][1].split(sep='\\')[-1],
                                    "SNR": self.target_SNR,
                                    "correct": ans,
                                    "turning_points": self.turning_points},
                                   ignore_index=True)

        if ans:
            self.target_SNR -= self.step
        else:
            self.target_SNR += self.step

        if self.verbose:
            os.system('cls')
            print(self.log[['play_count', 'SNR', 'correct', 'turning_points']])

        if self.turning_points == self.stop_after:
            self.stop_and_save()

        self.play_count = 0
        self.prepare_mix()

    def stop_and_save(self):
        self.log.to_csv('results.csv', index=True, header=True, encoding='utf-8')
        messagebox.showinfo('Koniec eksperymentu',
                            'Koniec eksperymentu 19/EXP01\n'
                            'Serdecznie dziękuję!')
        global root
        root.destroy()


def bind_keys():
    global root
    root.bind('s', apka.same)
    root.bind('S', apka.same)
    root.bind('d', apka.different)
    root.bind('D', apka.different)
    root.bind('<space>', apka.play)


root = Tk()
root.title('19/EXP01')

apka = App(root)

bind_keys()

apka.mainloop()
