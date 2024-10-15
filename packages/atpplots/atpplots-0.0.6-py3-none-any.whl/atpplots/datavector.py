import numpy as np

try:
    import plotly.graph_objects as go
except ImportError:
    pass

try:
    import holoviews as hv

    hv.extension("bokeh")
except ImportError:
    pass


interpolation_methods = {
    "linear": {"hv": "linear", "plotly": ""},
    "ffill": {"hv": "steps-post", "plotly": ""},
    "bfill": {"hv": "steps-pre", "plotly": ""},
}


class DataVector:
    def __init__(
        self,
        data_x: list | np.ndarray | None = None,
        data_y: list | np.ndarray | None = None,
        color: str = "blue",
        label: str = "",
        interpolation: str = "linear",
        mode: str = "lines",
        alpha: float = 1.0,
        thickness: int = 1,
        line_style: str = "-",
    ):
        if interpolation not in interpolation_methods.keys():
            raise ValueError(
                f"Interpolation method '{interpolation}' is not supported."
            )
        self.data_x: list | np.ndarray | None = data_x
        self.data_y: list | np.ndarray | None = data_y

        self.color: str = color
        self.label: str = label
        self.mode: str = mode  # TODO: lines, markers, lines+markers
        self.interpolation: str = interpolation
        self.alpha: float = alpha
        self.thickness: int = thickness
        self.line_style: str = line_style

        return None

    # if plotly is available we can add this method to the class

    if "go" in globals():

        def to_plotly_scatter(self) -> go.Scatter:
            ret = go.Scatter(
                x=self.data_x,
                y=self.data_y,
                mode=self.mode,
                name=self.label,
                line={"color": self.color},
            )
            return ret

    if "hv" in globals():

        def to_holoviews_scatter(
            self,
            kdims: list | None = None,
            vdims: list | None = None,
        ) -> hv.Curve:
            ret = hv.Curve(
                (self.data_x, self.data_y),
                kdims=kdims,
                vdims=vdims,
                label=self.label,
            ).opts(
                color=self.color,
                interpolation=interpolation_methods[self.interpolation]["hv"],
            )
            return ret
