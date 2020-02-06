# TODO: normalize all audio files by RMS (future?)

import os
from scipy.io.wavfile import read, write
import pyloudnorm as pyln
import time


start_time = time.time()
corename = 'D:\\phd\\DATA'
recordings_core = '\\test_recordings'

# create BS.1770 meter
meter = pyln.Meter(44100)

for speaker_directory in os.listdir(corename + recordings_core):

    for wavname in os.listdir(corename + recordings_core + '\\' + speaker_directory):

        # load wave
        rate, signal = read(corename + recordings_core + '\\' + speaker_directory + '\\' + wavname)

        # librosa:: preprocessing (conversion to float)
        signal = signal / float(2 ** 15)

        # normalize audio to -12 dB LUFS
        signal = pyln.normalize.loudness(signal, meter.integrated_loudness(signal), -12.0)
        write(corename + recordings_core + '\\' + speaker_directory + '\\_norm_' + wavname,
              rate,
              signal)

        print('Recording {} done'.format(wavname))

print('--- %s seconds ---' % (time.time() - start_time))
