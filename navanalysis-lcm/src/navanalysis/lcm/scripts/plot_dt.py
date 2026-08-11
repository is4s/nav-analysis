#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from aspn23_xtensor import TypeTimestamp, to_seconds
from lcm import Event, EventLog
from navanalysis.lcm.measurements import decode_aspn_lcm_msg
from navanalysis.lcm.plots.utils import save_or_show
from tqdm import tqdm


def plot_dt(logfile: str, save_dir=None) -> None:
    log = EventLog(logfile, 'r')

    times: dict[str, list[TypeTimestamp]] = {}
    t0 = None

    msg: Event
    log_size = log.size()
    progressbar = tqdm(total=log_size, unit='B', unit_scale=True)
    fpos = log.tell()
    for msg in log:
        new_fpos = log.tell()
        progressbar.update(new_fpos - fpos)
        fpos = new_fpos

        t, aspn_msg = decode_aspn_lcm_msg(msg)

        if t is not None:
            if msg.channel not in times:
                if t0 is None:
                    t0 = t
                times[msg.channel] = []
            times[msg.channel].append(t)

    for channel, time in times.items():
        time = np.array(time)
        rel_time = np.array([to_seconds(t - t0) for t in time])
        dt = np.diff(rel_time)

        total_dt = rel_time[-1] - rel_time[0]
        N = len(rel_time)
        avg_dt = total_dt / (N - 1)
        plt.figure(f'DT {channel}')
        plt.suptitle(f'DT {channel}\n(avg = {avg_dt:.9f}s)')
        plt.scatter(rel_time[1:], dt, marker='.', label=channel)
        plt.xlabel('Time (s)')
        plt.ylabel('DT (s)')
        print(f'Avg dt for {channel}: {avg_dt:.9f}s')

    plt.legend()
    save_or_show(save_dir)


def main():
    parser = argparse.ArgumentParser(description="""Plot dt messages from LCM log.""")

    parser.add_argument('logfile', help='LCM log file.')
    parser.add_argument(
        '-a',
        '--all',
        help='Plot all altitude messages in log. If not set, will prompt user to determine which altitude channels should be plotted.',
        action='store_true',
    )

    parser.add_argument(
        '-s',
        '--save',
        nargs='?',
        const='.',
        default=None,
        metavar='DIR',
        help=(
            'Save plots as PNG files instead of showing them interactively. '
            'Optionally provide a directory to save into (default: current directory).'
        ),
    )

    args = parser.parse_args()
    log_data = sys.argv[1]
    plot_dt(log_data, save_dir=args.save)


if __name__ == '__main__':
    main()
