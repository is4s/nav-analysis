#!/usr/bin/env python3
import sys

from lcm import Event, EventLog


def get_channels(logfile: str) -> list[str]:
    """Get a list of the channels contained in the LCM log.

    Args:
        logfile: Path to LCM log

    Returns:
        list[str]: List of channels in the order they appeared in the log
    """
    read_log = EventLog(logfile, 'r')

    channels = []
    msg: Event
    for msg in read_log:
        if not msg.channel in channels:
            channels.append(msg.channel)
    read_log.close()

    return channels


def print_channels(logfile: str, sort: bool = True):
    """Print the channels found in an LCM log.

    Args:
        logfile: Path to LCM log.
        sort: Whether to sort the channels alphabetically before printing. If False, channels will be printed in the order they were found in the log.
    """
    channels = get_channels(logfile)
    if sort:
        channels.sort()

    print(f'Channels in {logfile}:')
    for channel in channels:
        print(f'\t{channel}')


def main():
    if len(sys.argv) != 2:
        print('Please provide an lcm log file.')
        exit()

    filename = sys.argv[1]
    print_channels(filename)


if __name__ == '__main__':
    main()
