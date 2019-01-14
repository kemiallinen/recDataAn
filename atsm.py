from scipy.io.wavfile import read
import numpy as np
from audiotsm.io.array import ArrayReader, ArrayWriter
from audiotsm import phasevocoder


wavname = 'C:\\Users\\Niemiec\\Documents\\PHD\\DATA\\recordings\\01_ZL\\01_ZL_001.wav'

# rate, signal = read(wavname)
signal = np.random.randn(2048)
print(signal.shape)

x = signal.reshape(1, signal.shape[0])
print(x.shape)

reader = ArrayReader(x)
writer = ArrayWriter(channels=1)

tsm = phasevocoder(reader.channels, speed=2)
tsm.run(reader, writer)
out = writer.data
out = out.flatten()
print(out.shape)
