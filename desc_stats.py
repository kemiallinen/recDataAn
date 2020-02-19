import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


db = pd.read_csv('D:\\phd\\phdDB.csv', sep=',')
mods = ['l', 'n', 'h']
params = ['F0_mean', 'HNR', 'jitter']
colors = ['cornflowerblue', 'seagreen', 'palevioletred']

id = '10_MS'

for idf, param in enumerate(params):
    db_slice = db[db['id'] == id][['mod', param]]

    fig, axs = plt.subplots(2, 2, num=idf)
    axs = axs.reshape(4,)
    if param == 'F0_mean':
        hist_range = (int(db_slice[param].min() / 5) * 5,
                      int(db_slice[param].max() / 5) * 5 + 5)
        num_bins = int(np.diff(hist_range) / 5)
    else:
        num_bins = 30
        hist_range = None
    ana = db_slice.groupby('mod')

    for idx, mod in enumerate(mods):
        axs[idx].hist(ana.get_group(mod)[param],
                      bins=20, alpha=0.7, density=1,
                      facecolor=colors[idx])
        axs[idx].set_title('mod = {}'.format(mod.upper()))
        axs[3].hist(ana.get_group(mod)[param],
                    bins=num_bins, density=1,
                    range=hist_range,
                    alpha=0.7, facecolor=colors[idx])
        axs[3].set_title('all mods')
    fig.suptitle(param)

plt.show()
