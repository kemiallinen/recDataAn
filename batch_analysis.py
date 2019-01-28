from librosa.feature import mfcc
from librosa.display import specshow
import librosa
import numpy as np
from pandas import DataFrame
import pandas as pd
import csv
import os
from scipy.io.wavfile import read
from matplotlib.pyplot import figure, savefig, axis, close
from Signal_Analysis.features.signal import get_F_0, get_HNR, get_Jitter

corename = 'D:\\phd\\DATA'
recordings_core = '\\test_recordings'
speakers_csvname = 'D:\\phd\\SpeakerData.csv'

speakers = pd.read_csv(speakers_csvname, sep=';', index_col=0)

# create dataframe
df = DataFrame(columns=["id", "sex", "path", "sentence", "mod",
                        "F0_mean", "HNR", "jitter", "MFCC", "specgram"])

for speaker_directory in os.listdir(corename + recordings_core):

    # read csv file containing sentences and mod info (n/h/l)
    txtfname = '\\sentences\\' + speaker_directory[:2] + '.csv'
    sentences = []

    speaker_sex = speakers['sex'].loc[speakers['prefix'] == speaker_directory].values[0]

    with open(corename + txtfname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            sentences.append(row)

    # prepare dirs for mfccs and specgrams
    mfcc_dir_name = '\\mfcc\\' + speaker_directory
    if not os.path.isdir(corename + mfcc_dir_name):
        os.mkdir(corename + mfcc_dir_name)

    specgram_dir_name = '\\specgrams\\' + speaker_directory
    if not os.path.isdir(corename + specgram_dir_name):
        os.mkdir(corename + specgram_dir_name)

    for wavname in os.listdir(corename + recordings_core + '\\' + speaker_directory):

        # load wave
        rate, signal = read(corename + recordings_core + '\\' + speaker_directory + '\\' + wavname)

        # get f0, Harmonic-to-Noise Ratio (HNR) and jitter values
        recF0mean = get_F_0(signal, rate, min_pitch=70, max_pitch=600)
        hnr = get_HNR(signal, rate)
        jttr = get_Jitter(signal, rate)

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
        recMFCC = mfcc(signal)
        np.save(corename + mfcc_dir_name + '\\' + wavname[-10:-4], recMFCC)

        # export data to pandas dataframe
        count = int(wavname[-7:-4])-1
        df = df.append({"id": wavname[:-8],
                        "sex": speaker_sex,
                        "path": recordings_core + '\\' + speaker_directory + '\\' + wavname,
                        "sentence": sentences[count][0],
                        "mod": sentences[count][1][0],
                        "F0_mean": recF0mean[0],
                        "HNR": hnr,
                        "jitter": [jttr],
                        "MFCC": mfcc_dir_name + '\\' + wavname[-10:-4] + '.npy',
                        "specgram": specgram_dir_name + '\\' + wavname[-10:-4] + '.png'},
                       ignore_index=True)

        print('Recording {} done'.format(wavname))

df.to_csv('D:\\phd\\phdDB_test.csv', index=True, header=True, encoding='utf-8')
