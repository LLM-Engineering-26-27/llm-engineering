"""Tests for plotting utilities."""

from llm_engineering.utils.plotting import plot_loss_curve


class TestPlotLossCurve:
    def test_creates_figure(self):
        fig = plot_loss_curve(
            steps=[0, 1, 2, 3],
            losses=[2.5, 2.0, 1.5, 1.2],
        )
        assert fig is not None
        assert len(fig.axes) == 1

    def test_save_to_file(self, tmp_path):
        fig = plot_loss_curve(
            steps=[0, 1, 2],
            losses=[3.0, 2.0, 1.0],
        )
        path = tmp_path / "loss.png"
        fig.savefig(path)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_with_title(self):
        fig = plot_loss_curve(
            steps=[0, 1],
            losses=[2.0, 1.0],
            title="Test Loss",
        )
        assert fig.axes[0].get_title() == "Test Loss"
