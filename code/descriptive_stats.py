#!/usr/bin/python3

from os.path import join as opj
import numpy as np


def timestamp2sec(ts, fps=25):
    '''Convert timestamp to time in seconds.

    Parameters
    ----------
    ts : str
      time stamp in format HH:MM:SS:Frame
    fps : int
      number of frames per second

    Returns
    -------
    float
      Time in seconds.
    '''
    hh, mm, ss, frame = ts.split(b':')
    seconds = \
        (int(hh) * 60 * 60) \
        + (int(mm) * 60) \
        + int(ss) \
        + (float(frame) / fps)
    return seconds


def load_annotations(fname=opj('data', 'structure.csv')):
    annot = np.recfromcsv(fname)
    times = [timestamp2sec(t) for t in annot['time']]
    # do a little dance to get timestamps as floating point seconds
    # in the recarray
    annot['time'] = [0] * len(times)
    # convert dtype for time
    dt = annot.dtype.descr
    dt[0] = (dt[0][0], 'float64')
    dt = np.dtype(dt)
    annot = annot.astype(dt)
    # reassign converted timestamps over the dummy zeros
    annot['time'] = times
    return annot


# tex format help
def _ft(key, value, fmt='s'):
    val_tmpl = '{{{{value:{}}}}}'.format(fmt)
    tex = '\\newcommand{{{{\\{{key}}}}}}{{{val_tmpl}}}'.format(val_tmpl=val_tmpl)
    return tex.format(key=key, value=value)


def print_descriptive_stats_as_tex(annot):
    print(_ft('NShots', len(annot), 'd'))


if __name__ == '__main__':
    data = load_annotations()
    print_descriptive_stats_as_tex(data)
