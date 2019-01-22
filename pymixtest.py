# import pygame
from scipy.io.wavfile import read
# from pygame.sndarray import make_sound
import sounddevice as sd
import numpy as np

sd.default.samplerate = 44100
sd.default.device = 4
# pygame.init()
# pygame.mixer.pre_init(frequency=44100, channels=1)
# print(pygame.mixer.get_init())
# pygame.mixer.music.stop()
print(sd.query_devices())
print('\n')
rate, signal = read('D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_001.wav')

signal = np.require(signal, requirements='W')
print(np.max(signal))
print(len(signal))
signal = signal/np.max(np.abs(signal))
# print(np.max(signal))
print(np.max(signal))
print(len(signal))
sd.play(signal, samplerate=rate)
# sound = make_sound(signal)
#
# x = pygame.mixer.Sound(sound)
# x.play(0, 0.0)
