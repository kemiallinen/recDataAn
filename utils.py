import numpy as np
from Signal_Analysis.features.signal import get_F_0


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


def f0(signal_buffered, rate, win_len, window):
    arr_f0 = {'t': [], 'freq': []}
    current_time = 0

    for signalSnippet in np.transpose(signal_buffered):
        signalSnippet *= window
        pitch = get_F_0(signalSnippet, rate, min_pitch=50, max_pitch=800, pulse=False)[0]
        current_time += win_len / 2
        arr_f0['t'].append(round(current_time, 4))
        arr_f0['freq'].append(pitch)

    f0mean = np.round(np.sum(arr_f0['freq']) / float(np.count_nonzero(arr_f0['freq'])), 2)

    return f0mean, arr_f0
