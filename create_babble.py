import pandas as pd
import numpy as np
from scipy.io.wavfile import read, write
from random import randint
from utils import rms

db = pd.read_csv('D:\\phd\\phdDB_test.csv', sep=',', index_col=0)
corename = 'D:\\phd\\DATA'
fs = 44100
rms_target = 30
slice_len = int(0.2 * fs)
out = []

for i in range(50):
    out_second = np.zeros(slice_len, dtype='float32')
    for num_path, path in enumerate(db['path']):
        print('{} iter, speaker {} out of {}'.format(i + 1, num_path + 1, len(db['path'])))
        _, single_utter = read(corename + path)
        single_utter_norm = single_utter * (rms_target / rms(single_utter))
        startpt = randint(0, len(single_utter) - slice_len)
        slice_utter = single_utter_norm[startpt: startpt + slice_len]
        slice_utter /= (2**15 * len(db['path']))
        out_second += slice_utter
    out = np.concatenate((out, out_second))

out *= 2**15
out = out.astype(dtype='int16')
write('babble.wav', fs, out)
