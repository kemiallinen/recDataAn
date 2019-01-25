import pygame
from scipy.io.wavfile import read
from pygame.sndarray import make_sound
import numpy as np


pygame.mixer.pre_init(frequency=44100, channels=1)
pygame.mixer.init()
print(pygame.mixer.get_init())

rate, first_signal = read('D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_001.wav')
_, second_signal = read('D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_002.wav')

signal = np.concatenate((first_signal, second_signal))
signal += np.random.randint(-2**13, 2**13, size=signal.shape, dtype='int16')

sound_object = make_sound(signal)
pygame.mixer.stop()
pygame.mixer.Sound(sound_object).play()
# pygame.mixer.quit()
