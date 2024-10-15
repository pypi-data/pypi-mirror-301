import holoviews as hv
import plotly.graph_objects as go
from bokeh.plotting import figure as bokeh_figure

from .axis import Axis
from .datavector import DataVector
from .figure import Figure

hv.extension("bokeh")


class CurveDataVector(Figure):
    def __init__(
        self,
        data_vectors: DataVector | list[DataVector],
        axis_x: str | Axis | dict = "X",
        axis_y: str | Axis | dict = "Y",
        **kwargs,
    ):
        Figure.__init__(
            self,
            **kwargs,
        )

        self.axis_x = Axis.init(axis_x)
        self.axis_y = Axis.init(axis_y)

        if not isinstance(data_vectors, list):
            data_vectors = [data_vectors]
        self.data_vectors = data_vectors

        return None

    def to_holoviews(self) -> hv.Overlay:
        ret = []

        for data_vector in self.data_vectors:
            curve = data_vector.to_holoviews_scatter(
                kdims=[self.axis_x.hv_dimension],
                vdims=[self.axis_y.hv_dimension],
            )

            ret.append(curve)

        return hv.Overlay(ret).opts(
            width=self.width,
            height=self.height,
            title=self.title,
        )

    def to_bokeh(self):
        fig: bokeh_figure = bokeh_figure(
            title=self.title,
            width=self.width,
            height=self.height,
            # x_axis_type="datetime",
            y_axis_type=self.axis_y.scale,
            x_axis_type=self.axis_x.scale,
        )

        for data_vector in self.data_vectors:
            fig.line(
                x=data_vector.data_x,
                y=data_vector.data_y,
                legend_label=data_vector.label,
                color=data_vector.color,
                alpha=data_vector.alpha,
                line_width=data_vector.thickness,
            )

        fig.legend.location = "top_left"
        fig.legend.title = "Signal type"
        fig.legend.title_text_font_style = "bold"
        fig.legend.title_text_font_size = "20px"
        # range
        if self.axis_y.range_min:
            fig.y_range.start = self.axis_y.range_min
        if self.axis_y.range_max:
            fig.y_range.end = self.axis_y.range_max

        # axis labels
        fig.xaxis.axis_label = self.axis_x.label
        fig.yaxis.axis_label = self.axis_y.label
        # axis scale

        return fig

    def _plotly_figure(self) -> go.Figure:
        fig = go.Figure()
        fig.update_layout(
            title=self.title,
            width=self.width,
            height=self.height,
            showlegend=self.showlegend,
        )
        fig.update_xaxes(
            title_text=self.axis_x.label,
            range=self.axis_x.range,
            type=self.axis_x.scale,
        )
        fig.update_yaxes(
            title_text=self.axis_y.label,
            range=self.axis_y.range,
            type=self.axis_y.scale,
        )
        return fig

    def to_plotly(self) -> go.Figure:
        fig = self._plotly_figure()

        for data_vector in self.data_vectors:
            fig.add_trace(data_vector.to_plotly_scatter())

        return fig
