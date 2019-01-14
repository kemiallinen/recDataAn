from scipy.io.wavfile import read
import librosa

zaleN = list(range(301, 401))
zaleH = list(range(201, 301))
zaleL = list(range(401, 501))

adkuN = list(range(201, 251))
adkuN.extend(range(301, 351))
adkuH = list(range(101, 201))
adkuL = list(range(251, 301))
adkuL.extend(range( 361, 411))

zale=[]
dirname = 'C:\\Users\\Niemiec\\Documents\\PHD\\recordings\\01_ZL\\'

for i in zaleN:
    fname = dirname + '01_ZL_' + str(i) + '.wav'
    zale.append([read(fname), 'N'])
    print('01_ZL_' + str(i) + '.wav' + ' read')
for i in zaleH:
    fname = dirname + '01_ZL_' + str(i) + '.wav'
    zale.append([read(fname), 'H'])
    print('01_ZL_' + str(i) + '.wav' + ' read')
for i in zaleL:
    fname = dirname + '01_ZL_' + str(i) + '.wav'
    zale.append([read(fname), 'L'])
    print('01_ZL_' + str(i) + '.wav' + ' read')

