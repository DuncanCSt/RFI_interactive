import matplotlib.pyplot as plt
import pandas as pd


def plot_summary_with_transitions(
        summary_df: pd.DataFrame,
        transitions_df: pd.DataFrame,
        x_range: tuple = (1000, 1600)
    ) -> tuple[plt.Figure, plt.Axes]:
    """Return a matplotlib figure showing ``summary_df`` and ``transitions_df``.

    Vertical lines indicate the frequencies from ``transitions_df``.
    """
    fig, ax = plt.subplots()
    ax.plot(summary_df['frequency'], summary_df['mean'], alpha=0.5, label='Mean')
    plt.fill_between(
        summary_df['frequency'],
        summary_df['mean'] - summary_df['std'],
        summary_df['mean'] + summary_df['std'],
        alpha=0.2,
        label='1 std',
    )

    ax.scatter(
        summary_df['frequency'], summary_df['trace_1'], 
        alpha=0.5, s=1, label='Traces'
    )
    for col in ['trace_' + str(i) for i in range(2, 4)]:
        ax.scatter(summary_df['frequency'], summary_df[col], alpha=0.5, s=1)

    for frequency in transitions_df['Frequency (MHz)']:
        ax.axvline(x=frequency, color='red', linestyle='--', alpha=0.5)

    ax.set_xlabel("Frequency")
    ax.set_ylabel("Mean (log rescaled)")
    ax.set_title("Mean vs Frequency")
    ax.legend()
    ax.set_xlim(x_range)
    return fig, ax
