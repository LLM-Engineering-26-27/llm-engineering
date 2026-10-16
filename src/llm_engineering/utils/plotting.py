"""Plotting utilities for training metrics.

Provides a reusable function for plotting loss curves. Uses matplotlib for
static plots. Grows weekly as new visualizations are needed (attention maps,
scaling plots, etc.).
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_loss_curve(
    steps: list[int],
    losses: list[float],
    title: str = "Loss Curve",
) -> Figure:
    """Plot a loss curve.

    Args:
        steps: x-axis values.
        losses: loss values.
        title: Plot title.

    Returns:
        A matplotlib Figure.
    """
    fig, ax = plt.subplots()

    ax.plot(steps, losses)

    ax.set_title(title)
    ax.set_xlabel("Step")
    ax.set_ylabel("Loss")
    plt.close(fig)
    return fig
