#!/usr/bin/python3

from os.path import join as opj
import numpy as np
import itertools


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


def _get_n_reoccurrences(vals):
    return [len(list(i[1])) - 1  # subtract one for the first occurrence
            # loop over each unique value
            for i in itertools.groupby(
                # sort for next grouping
                sorted([i[0]
                        # get blocks of consecutive identical values
                        for i in itertools.groupby(vals)]))]


def _get_counts(vals):
    return [len(list(v))
            for k, v in itertools.groupby(sorted(vals))]


def _get_counts_consecutive(vals):
    return [len(list(v))
            for k, v in itertools.groupby(vals)]


def _print_location_info(vals, label):
    locations = np.unique(vals)
    print('% QA unique: {}'.format(repr(list(locations))))
    print(_ft('N{}s'.format(label), len(locations), 'd'))
    # revisited locations
    # shots per location
    # consecutive shots per location
    for fx, proplabel in (
            (_get_n_reoccurrences, 'NTimes{}sRevisited'),
            (_get_counts, 'ShotsPer{}'),
            (_get_counts_consecutive, 'ConsecShotsPer{}')):
        freq = fx(vals)
        proplabel = proplabel.format(label)
        print(_ft('{}Mean'.format(proplabel), np.mean(freq), '.1f'))
        print(_ft('{}Min'.format(proplabel), min(freq), '.0f'))
        print(_ft('{}Max'.format(proplabel), max(freq), '.0f'))
        print(_ft('{}Median'.format(proplabel), np.median(freq), '.0f'))


def print_descriptive_stats_as_tex(data):
    print(_ft('NShots', len(data), 'd'))
    shot_durations = np.diff(data['time'])
    print(_ft('ShotLengthMedian', np.median(shot_durations), '.2f'))
    print(_ft('ShotLengthMin', shot_durations.min(), '.2f'))
    print(_ft('ShotLengthMax', shot_durations.max(), '.2f'))
    print(_ft('ShotLengthSD', shot_durations.std(), '.2f'))
    # without paramount and final black frame
    _print_location_info(shots[1:-1]['major_location'], 'MajorLocation')
    _print_location_info(shots[1:-1]['setting'], 'Setting')
    _print_location_info(shots[1:-1]['locale'], 'Locale')

    # interior/exterior
    print('% QA unique: {}'.format(np.unique(shots[1:-1]['int_or_ext'])))
    print(_ft('NExteriorShots', sum(shots[1:-1]['int_or_ext'] == b'ext'), 'd'))
    print(_ft('NInteriorShots', sum(shots[1:-1]['int_or_ext'] == b'int'), 'd'))

    # time of day
    print('% QA unique: {}'.format(np.unique(shots[1:-1]['time_of_day'])))
    print(_ft('NDayShots', sum(shots[1:-1]['time_of_day'] == b'day'), 'd'))
    print(_ft('NNightShots', sum(shots[1:-1]['time_of_day'] == b'night'), 'd'))

    # time
    print('% QA unique: {}'.format(np.unique(shots[1:-1]['flow_of_time'])))
    for c, label in ((b'0', 'NoJump'), (b'+', 'SmallJump'),
                     (b'++', 'LargeJump'), (b'-', 'Flashback')):
        print(_ft('NShotsTime{}'.format(label),
                  sum(shots[1:-1]['flow_of_time'] == c),
                  'd'))


if __name__ == '__main__':
    shots = load_annotations()
    print_descriptive_stats_as_tex(shots)
