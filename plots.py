import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_summary_with_transitions(
        summary_df: pd.DataFrame,
        transitions_df: pd.DataFrame,
        x_range: tuple = (1000, 1600)
    ) -> tuple[plt.Figure, plt.Axes]:
    """
    Return a matplotlib figure showing a downsampled version of summary_df and vertical
    lines for frequencies from transitions_df. The downsampling is done by finding the closest
    row indexes corresponding to x_range boundaries and then selecting at most 1000 rows.
    Assumes summary_df is already sorted by 'frequency'.
    """
    # Find the positional indexes closest to the x_range boundaries.
    low_index = summary_df['frequency'].searchsorted(x_range[0], side='left')
    high_index = summary_df['frequency'].searchsorted(x_range[1], side='right') - 1

    # Clamp indexes to valid range.
    low_index = max(low_index, 0)
    high_index = min(high_index, len(summary_df) - 1)

    # Generate at most 200 equally spaced integer row positions between low_index and high_index.
    # np.linspace returns float values; casting to int and applying np.unique removes duplicates.
    indices = np.unique(np.linspace(low_index, high_index, 1000).astype(int))
    downsampled = summary_df.iloc[indices]

    fig, ax = plt.subplots()
    ax.plot(downsampled['frequency'], downsampled['mean'],
            alpha=0.5, label='Mean')
    ax.plot(downsampled['frequency'], downsampled['baseline'],
            alpha=0.5, label='Baseline', c='black')
    plt.fill_between(
        downsampled['frequency'],
        downsampled['mean'] - downsampled['std'],
        downsampled['mean'] + downsampled['std'],
        alpha=0.2, label='1 std',
    )

    ax.scatter(downsampled['frequency'], downsampled['trace_1'],
               alpha=0.5, s=1, label='Traces')
    for col in ['trace_' + str(i) for i in range(2, 4)]:
        ax.scatter(downsampled['frequency'], downsampled[col],
                   alpha=0.5, s=1)

    # Plot vertical lines for transitions within the specified x_range.
    for frequency in transitions_df['Frequency (MHz)']:
        if x_range[0] <= frequency <= x_range[1]:
            ax.axvline(x=frequency, color='red', linestyle='--', alpha=0.5)

    ax.set_xlabel("Frequency")
    ax.set_ylabel("Mean (log rescaled)")
    ax.set_title("Mean vs Frequency")
    ax.legend()
    return fig, ax
