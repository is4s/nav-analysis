from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def get_statistics(arr: np.ndarray):
    """
    Generate the following statistics from a given array of values:
    1) Mean
    2) Standard Deviation
    3) Root Mean Square
    4) Absolute Max

    Args:
        - arr (np.ndarray): Array for which to generate statistics.

    Returns:
        - String containing the generated statistics.
    """
    m = np.nanmean(arr)
    std = np.nanstd(arr)
    rms = np.sqrt(np.nansum(np.square(arr)) / np.count_nonzero(np.isfinite(arr)))
    abs_max = np.nanmax(np.abs(arr))

    statistics_str = (
        f'Mean: {m:.2f}\n'
        + f'Standard Deviation: {std:.2f}\n'
        + f'Root Mean Square: {rms:.2f}\n'
        + f'Absolute Max: {abs_max:.2f}'
    )

    return statistics_str


def show_stats(fig: Figure, y: np.ndarray):
    plt.subplots_adjust(right=0.7)
    ax_pos = plt.gca().get_position()
    x_pos = ax_pos.xmax + 0.01
    y_pos = ax_pos.ymin + 0.01
    stats = get_statistics(y)
    fig.text(x_pos, y_pos, stats)


def save_or_show(save_dir=None):
    """Either save all open figures to save_dir, or show them interactively.

    Args:
        save_dir: If None, calls plt.show(). Otherwise, saves every open
            figure as a PNG into save_dir (created if it doesn't exist),
            using each figure's label as the filename.
    """
    if save_dir is None:
        plt.show()
        return

    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        label = fig.get_label() or f'figure_{fig_num}'
        safe_name = (
            ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in label)
            .strip()
            .replace(' ', '_')
        )
        out_path = save_dir / f'{safe_name}.png'
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        print(f'Saved {out_path}')

    plt.close('all')
