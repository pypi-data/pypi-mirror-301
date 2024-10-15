from __future__ import annotations

import holoviews as hv


class Axis:
    def __init__(
        self,
        title: str,
        id: str = "",
        unit: str | None = None,
        shared: bool = False,
        range_min: float | None = None,
        range_max: float | None = None,
        scale: str = "linear",
    ):
        if scale not in ["linear", "log"]:
            raise ValueError(f"Scale method '{scale}' is not supported.")
        self.scale = scale
        self.id = id
        self.title = title
        self.unit = unit
        self.shared = shared
        self.range_min = range_min
        self.range_max = range_max
        self.range = [self.range_min, self.range_max]

        return None

    @property
    def label(self) -> str:
        if self.unit is None:
            return self.title

        return f"{self.title} [{self.unit}]"

    @property
    def hv_dimension(self) -> hv.Dimension:
        if self.id == "" or self.id is None:
            return hv.Dimension(self.label)
        return hv.Dimension(self.id, label=self.label)

    @classmethod
    def init(cls, input: str | dict | Axis) -> Axis:
        if isinstance(input, Axis):
            return input
        elif isinstance(input, str):
            return Axis(id=input, title=input)
        elif isinstance(input, dict):
            return Axis(**input)
        else:
            raise ValueError(f"Invalid axis type: {type(input)}")
