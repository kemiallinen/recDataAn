from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from Signal_Analysis.features.signal import get_F_0
from librosa.feature import mfcc
from librosa.display import specshow
from pymongo import MongoClient
import librosa


def buffer(x, n, p=0, opt=None):
    """Mimic MATLAB routine to generate buffer array

    MATLAB docs here: https://se.mathworks.com/help/signal/ref/buffer.html

    Args
    ----
    x:   signal array
    n:   number of data segments
    p:   number of values to overlap
    opt: initial condition options. default sets the first `p` values
         to zero, while 'nodelay' begins filling the buffer immediately.
    """
    import numpy

    if p >= n:
        raise ValueError('p ({}) must be less than n ({}).'.format(p, n))

    # Calculate number of columns of buffer array
    cols = int(numpy.ceil(len(x)/float(n-p)))

    # Check for opt parameters
    if opt == 'nodelay':
        # Need extra column to handle additional values left
        cols += 1
    elif opt is not None:
        raise SystemError('Only `None` (default initial condition) and '
                          '`nodelay` (skip initial condition) have been '
                          'implemented')

    # Create empty buffer array
    b = numpy.zeros((n, cols))

    # Fill buffer by column handling for initial condition and overlap
    j = 0
    for i in range(cols):
        # Set first column to n values from x, move to next iteration
        if i == 0 and opt == 'nodelay':
            b[0:n, i] = x[0:n]
            continue
        # set first values of row to last p values
        elif i != 0 and p != 0:
            b[:p, i] = b[-p:, i-1]
        # If initial condition, set p elements in buffer array to zero
        else:
            b[:p, i] = 0

        # Get stop index positions for x
        k = j + n - p

        # Get stop index position for b, matching number sliced from x
        n_end = p+len(x[j:k])

        # Assign values to buffer array from x
        b[p:n_end, i] = x[j:k]

        # Update start index location for next iteration of x
        j = k

    return b


def f0(signalBuffered, rate, winLen, window, ifplot=False):
    arrF0 = {'t': [], 'freq': []}
    currentTime = 0

    for signalSnippet in np.transpose(signalBuffered):
        signalSnippet *= window
        pitch = get_F_0(signalSnippet, rate, min_pitch=50, max_pitch=800, pulse=False)[0]
        currentTime += winLen / 2
        arrF0['t'].append(round(currentTime, 4))
        arrF0['freq'].append(pitch)

    f0mean = np.round(np.sum(arrF0['freq']) / float(np.count_nonzero(arrF0['freq'])), 2)

    if ifplot:
        fig, ax1 = plt.subplots()
        color = 'tab:blue'
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('amplitude', color=color)
        ax1.plot(ts, signal, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('pitch [Hz]', color=color)
        ax2.plot(arrF0['t'], arrF0['freq'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        plt.title('mean pitch [Hz] = {}'.format(f0mean))
        fig.tight_layout()
        plt.show()

    return f0mean, arrF0


corename = 'C:\\Users\\Niemiec\\Documents\\PHD\\DATA'

# dla osoby
# txtfname = '\\recordings\\01_ZL\\01.txt'
# sentences = []
# textfile = open(corename+txtfname, 'r')
# for line in textfile:
#     fields = line.split('\t')
#     sentences.append(fields[1][:-1])
# textfile.close()

# dla nagrania
wavname = '\\recordings\\01_ZL\\01_ZL_001.wav'

rate, signal = read(corename + wavname)
ts = np.arange(0, len(signal)/float(rate), 1.0/rate)
winLen = 2*4096/44100
window = np.hanning(int(winLen*rate/2)*2)
signalBuffered = buffer(signal, len(window), int(len(window)/2))
recF0mean, recArrF0 = f0(signalBuffered, rate, winLen, window, ifplot=False)
# print(recF0mean)
# print(recArrF0['freq'])
#preprocessing (conversion to float for librosa)
signal = signal/float(2**15)

#librosa specgram
D = librosa.stft(signal)
plt.figure()
plt.subplot(211)
specshow(librosa.amplitude_to_db(librosa.magphase(D)[0], ref=np.max))
plt.axis('off')
plt.subplot(212)
plt.plot(recArrF0['t'], recArrF0['freq'])
plt.show()
# plt.savefig(corename + '\\specgrams\\' + wavname[-10:-4] + '.png', dpi=200)
# plt.close()

# #librosa MFCC
# recMFCC = mfcc(signal)
# np.save(corename + '\\mfcc\\' + wavname[-10:-4], recMFCC)
#
# #export data to mongodb
# client = MongoClient('mongodb://localhost:27017')
# db = client.data
# collection = db.data
# post = {"initials": wavname[-10:-8],
#         "path": wavname,
#         "sentence": sentences[int(wavname[-7:-4])-1],
#         "mod": "n",
#         "f0mean": recF0mean,
#         "f0t": recArrF0,
#         "mfcc": '\\mfcc\\' + wavname[-10:-4] + '.npy',
#         "specgram": '\\specgrams\\' + wavname[-10:-4] + '.png'}
# collection.insert_one(post).inserted_id
