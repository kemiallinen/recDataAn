import numpy as np
from librosa import load
from librosa import piptrack, ifgram
from librosa.display import specshow
import matplotlib.pyplot as plt

fname = 'C:\\Users\\Niemiec\\Documents\\PHD\\recordings\\01_ZL\\01_ZL_001.wav'
signal, rate = load(fname)
ts = np.arange(0, len(signal)/float(rate), 1.0/rate)

frequencies, D = ifgram(signal, rate)
specshow(frequencies)
plt.show()
# pitches, magnitudes = piptrack(y=signal,
#                                sr=rate,
#                                threshold=0.03,
#                                fmin=50,
#                                fmax=500)
# print(pitches)
# print(magnitudes)
# plt.subplot(211)
# plt.plot(pitches)
# plt.subplot(212)
# plt.plot(magnitudes)
# plt.show()