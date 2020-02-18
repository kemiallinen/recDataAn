import pandas as pd
import numpy as np
from scipy.io.wavfile import read, write
from random import randint


db = pd.read_csv('D:\\phd\\phdDB.csv', usecols=['sex', 'path', 'mod', 'sentence'])
corename = 'D:\\phd\\DATA'
fs = 44100
duration = 15

for sex in ['f', 'm']:
    for mod in ['n', 'l', 'h']:
        out = np.zeros(duration * fs, dtype='float32')
        for i in range(5):
            paths = db.loc[(db['sex'] == sex) & (db['mod'] == mod)]['path'].sample(frac=1)
            for num_path, path in enumerate(paths):
                print('{}-{} iter {} :: {} / {}'.format(sex, mod, i, num_path + 1, len(paths)))
                _, single_utter = read(corename + path)
                if randint(0, 1):
                    single_utter = single_utter[::-1]
                startpt = randint(-fs, (duration-1) * fs)
                if startpt < 0:
                    out[:len(single_utter) + startpt] += single_utter[-startpt:] / len(paths)
                elif startpt > duration * fs - len(single_utter):
                    out[startpt:] += single_utter[:duration * fs - startpt] / len(paths)
                else:
                    out[startpt:startpt + len(single_utter)] += single_utter / len(paths)
                print('')

        print('normalize [final]')
        out /= (np.max(np.abs(out)) / (2 ** 14))
        out = out.astype(dtype='int16')
        write('babble_{}_mod-{}.wav'.format(sex, mod), fs, out)
        print('saved to babble_{}_mod-{}.wav'.format(sex, mod))
