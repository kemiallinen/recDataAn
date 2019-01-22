# Basic Python Music Player - using tkinter and pygame
# source: https://github.com/aglla/pyprojects/blob/master/music-player.py

from tkinter import *
import tkinter.filedialog as tk
import tkinter.messagebox as tk2
import pygame
from scipy.io.wavfile import read
import sounddevice as sd
from pygame.sndarray import make_sound

playlist = []


class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)

        # self.create_widgets()
        self.playlistbox = Listbox(self, width=40, height=10,
                                   selectmode=SINGLE)  # TODO: ---> BROWSE, MULTIPLE, EXTENDED (p.379)
        for song in playlist:
            self.playlistbox.insert(END, song)

        self.grid(rowspan=5, columnspan=4)
        self.playlistbox.grid(row=1)
        self.playButton = Button(self, text='Play', command=self.play)
        self.loopButton = Button(self, text='Loop', command=self.loop)
        self.addButton = Button(self, text='Add', command=self.add)
        self.playButton.grid(row=4, column=0)
        self.loopButton.grid(row=4, column=1)
        self.addButton.grid(row=4, column=2)
        self.pack()

        # pygame initialize
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, channels=1)
        pygame.mixer.init(frequency=44100, channels=1)
        print(pygame.mixer.get_init())

    def play(self):
        # if (len(playlist) == 0):
        #     tk2.showinfo('Notice', 'No songs in your playlist!\nClick Add to add songs.')
        # else:
        pygame.mixer.music.stop()
        rate, signal = read('D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_001.wav')
        sound = make_sound(signal)

        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(0, 0.0)

    def loop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1, 0.0)

    def add(self):
        file = tk.askopenfilenames(initialdir='C:/Users/babbu/Downloads')
        songsTuple = root.splitlist(file)  # turn user's opened filenames into tuple
        songsList = list(songsTuple)  # convert to list
        # Add the full filename of songto playlist list, and a shortened version to the listBox
        for song in songsList:
            playlist.append(song);
            tempArray = song.split('/')
            songShort = tempArray[len(tempArray) - 1]
            self.playlistbox.insert(END, songShort)


root = Tk()
root.title('Text Editor')
root.geometry('500x200')
app = Application(root)
app.mainloop()
