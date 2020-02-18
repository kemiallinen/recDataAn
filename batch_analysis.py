from librosa.feature import mfcc, delta
from librosa.display import specshow
import librosa
import numpy as np
from matplotlib.pyplot import figure, savefig, axis, close
from pandas import DataFrame, read_csv
import os
from scipy.io.wavfile import read
from Signal_Analysis.features.signal import get_F_0, get_HNR, get_Jitter
import time


start_time = time.time()
corename = 'D:\\phd\\DATA'
recordings_core = '\\recordings'
speakers_csvname = 'D:\\phd\\SpeakerData.csv'
full_csvname = 'D:\\phd\\phdDB.csv'
skip = []

winlen = int(0.02 * 44100)
winshift = int(0.01 * 44100)
speakers = read_csv(speakers_csvname, sep=';', index_col=0)

# create dataframe
if not os.path.isfile(full_csvname):
    df = DataFrame(columns=["id", "sex", "path", "sentence", "mod",
                            "F0_mean", "HNR", "jitter", "MFCC_fv", "specgram"])
    df.to_csv(full_csvname, index=True, header=True, encoding='utf-8')

for speaker_directory in [x for x in os.listdir(corename + recordings_core) if x not in skip]:
    partial_start_time = time.time()
    # flush dataframe
    df = DataFrame(columns=["id", "sex", "path", "sentence", "mod",
                            "F0_mean", "HNR", "jitter", "MFCC_fv", "specgram"])

    # read csv file containing sentences and mod info (n/h/l)
    txtfname = '\\sentences\\' + speaker_directory[:2] + '.csv'
    speaker_sex = speakers['sex'].loc[speakers['prefix'] == speaker_directory].values[0]
    sentences = read_csv(corename + txtfname, sep=';', encoding='cp1250',
                         names=['sentence', 'mod'])

    # prepare dirs for mfccs and specgrams
    mfcc_dir_name = '\\mfcc\\' + speaker_directory
    if not os.path.isdir(corename + mfcc_dir_name):
        os.mkdir(corename + mfcc_dir_name)
    specgram_dir_name = '\\specgrams\\' + speaker_directory
    if not os.path.isdir(corename + specgram_dir_name):
        os.mkdir(corename + specgram_dir_name)

    # iterate through all recordings in a given directory
    for count, wavname in enumerate(sorted(os.listdir(corename + recordings_core + '\\' + speaker_directory))):
        print('--- {} --- {} ---'.format(wavname, sentences.iloc[count]['mod'].upper()))
        # load wave
        rate, signal = read(corename + recordings_core + '\\' + speaker_directory + '\\' + wavname)

        # get f0, Harmonic-to-Noise Ratio (HNR) and jitter values
        recF0mean = get_F_0(signal, rate)
        hnr = get_HNR(signal, rate)
        jttr = get_Jitter(signal, rate)['local']

        # librosa:: preprocessing (conversion to float)
        signal = signal / float(2 ** 15)

        # librosa:: generate specgram and save to relevant dir
        D = librosa.stft(signal)
        figure()
        specshow(librosa.amplitude_to_db(librosa.magphase(D)[0], ref=np.max))
        axis('off')
        savefig(corename + specgram_dir_name + '\\' + wavname[-10:-4] + '.png', dpi=200)
        close()

        # librosa:: calculate MFCC's (n_mfcc=20) and save *.npy file to relevant dir
        recMFCC = mfcc(signal, rate, n_mfcc=20, hop_length=winshift,
                       win_length=winlen, window=np.hamming(winlen))
        MFCC_feature_vector = np.concatenate((recMFCC,
                                              delta(recMFCC),
                                              delta(recMFCC, order=2)))
        np.save(corename + mfcc_dir_name + '\\' + wavname[-10:-4], MFCC_feature_vector)

        # export data to pandas dataframe
        df = df.append({"id": wavname[:-8],
                        "sex": speaker_sex,
                        "path": recordings_core + '\\' + speaker_directory + '\\' + wavname,
                        "sentence": sentences.iloc[count]['sentence'],
                        "mod": sentences.iloc[count]['mod'][0],
                        "F0_mean": round(recF0mean[0], 5),
                        "HNR": round(hnr, 5),
                        "jitter": round(jttr, 5),
                        "MFCC_fv": mfcc_dir_name + '\\' + wavname[-10:-4] + '.npy',
                        "specgram": specgram_dir_name + '\\' + wavname[-10:-4] + '.png'},
                       ignore_index=True)
        print('Recording {} done\n'.format(wavname))

    df.to_csv(full_csvname, mode='a', index=True, header=False, encoding='utf-8')
    print('Speaker {} done in {} seconds'.format(speaker_directory,
                                                 round(time.time() - partial_start_time, 2)))

print('--- process finished in %s minutes ---' % (round((time.time() - start_time) / 60, 2)))
