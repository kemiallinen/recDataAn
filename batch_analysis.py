from librosa.feature import mfcc
from librosa.display import specshow
import librosa
from pandas import DataFrame
import os
from scipy.io.wavfile import read
from utils import *

corename = 'D:\\phd\\DATA'
recordings_core = corename + '\\test_recordings'

df = DataFrame(columns=["initials", "path", "sentence", "mod",
                        "f0mean", "f0t", "mfcc", "specgram"])

for speaker_directory in os.listdir(recordings_core):

    # dla osoby
    txtfname = '\\sentences\\' + speaker_directory[:2] + '.txt'
    sentences = []
    textfile = open(corename + txtfname, 'r')
    for line in textfile:
        fields = line.split('\t')
        sentences.append(fields[1][:-1])
    textfile.close()

    mfcc_dir_name = corename + '\\mfcc\\' + speaker_directory
    if not os.path.isdir(mfcc_dir_name):
        os.mkdir(mfcc_dir_name)

    specgram_dir_name = corename + '\\specgrams\\' + speaker_directory
    if not os.path.isdir(specgram_dir_name):
        os.mkdir(specgram_dir_name)

    # dla nagrania
    for wavname in os.listdir(recordings_core + '\\' + speaker_directory):
        # wavname = '\\recordings\\01_ZL\\01_ZL_001.wav'

        rate, signal = read(recordings_core + '\\' + speaker_directory + '\\' + wavname)
        ts = np.arange(0, len(signal) / float(rate), 1.0 / rate)
        winLen = 2 * 4096 / 44100
        window = np.hanning(int(winLen * rate / 2) * 2)
        signalBuffered = buffer(signal, len(window), int(len(window) / 2))
        recF0mean, recArrF0 = f0(signalBuffered, rate, winLen, window)

        # preprocessing (conversion to float for librosa)
        signal = signal / float(2 ** 15)

        # librosa specgram
        D = librosa.stft(signal)
        plt.figure()
        specshow(librosa.amplitude_to_db(librosa.magphase(D)[0], ref=np.max))
        plt.axis('off')
        plt.savefig(specgram_dir_name + '\\' + wavname[-10:-4] + '.png', dpi=200)
        plt.close()

        # librosa MFCC
        recMFCC = mfcc(signal)
        np.save(mfcc_dir_name + '\\' + wavname[-10:-4], recMFCC)

        # export data to tinydb
        df = df.append({"initials": wavname[-10:-8],
                        "path": wavname,
                        "sentence": sentences[int(wavname[-7:-4]) - 1],
                        "mod": "n",
                        "f0mean": recF0mean,
                        "f0t": [recArrF0],
                        "mfcc": mfcc_dir_name + '\\' + wavname[-10:-4] + '.npy',
                        "specgram": specgram_dir_name + '\\' + wavname[-10:-4] + '.png'},
                       ignore_index=True)

        print(df)
        print('Recording {} done'.format(wavname))

df.to_csv('D:\\phd\\phdDB.csv', index=True, header=True, encoding='utf-8')
