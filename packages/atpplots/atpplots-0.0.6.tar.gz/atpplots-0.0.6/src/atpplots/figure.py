import holoviews as hv
import plotly.express as px
import plotly.graph_objects as go
from bokeh.plotting import show as bokeh_show


class Figure:
    def __init__(
        self,
        title: str | None = None,
        width: int | None = None,
        height: int | None = None,
        showlegend: bool = True,
    ):
        if title is None:
            title = ""
        if width is None:
            width = 1000
        if height is None:
            height = 600

        self.title: str = title
        self.width: int = width
        self.height: int = height
        self.showlegend: bool = showlegend
        return None

    # render
    def to_holoviews(self):
        raise NotImplementedError(
            "This method should be implemented in the child class."
        )

    def to_plotly(self) -> go.Figure:
        raise NotImplementedError(
            "This method should be implemented in the child class."
        )

    def to_bokeh(self):
        raise NotImplementedError(
            "This method should be implemented in the child class."
        )

    # show methods
    def show_holoviews(self):
        return bokeh_show(hv.render(self.to_holoviews()))

    def show_bokeh(self):
        return bokeh_show(self.to_bokeh())

    def show_plotly(self):
        return self.to_plotly().show()
