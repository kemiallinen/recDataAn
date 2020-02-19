import numpy as np
from librosa import load
from librosa.feature import mfcc, delta
from scipy.signal import hanning
# import matplotlib.pyplot as plt


filename = 'D:\\phd\\DATA\\recordings\\01_ZL\\01_ZL_001.wav'
y, sr = load(filename, sr=None)
winlen = int(0.02 * sr)
winshift = int(0.01 * sr)
mfccs = mfcc(y, sr, n_mfcc=20, hop_length=winshift, win_length=winlen, window=hanning(winlen))
feature_matrix = np.concatenate((mfccs,
                                 delta(mfccs),
                                 delta(mfccs, order=2)))

# TODO: RASTA-PLP
# print('size = {}'.format(mfccs.shape))

# plt.matshow(mfccs, aspect='auto')
# plt.show()
