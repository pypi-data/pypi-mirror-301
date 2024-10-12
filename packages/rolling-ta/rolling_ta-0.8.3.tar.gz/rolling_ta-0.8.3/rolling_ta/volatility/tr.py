from array import array
from typing import Literal, Union
from rolling_ta.extras.numba import _tr, _tr_update
from rolling_ta.indicator import Indicator
from rolling_ta.logging import logger
import pandas as pd
import numpy as np


class TR(Indicator):

    def __init__(
        self,
        data: pd.DataFrame,
        period_config: int = 14,
        memory: bool = True,
        retention: Union[int, None] = 20000,
        init: bool = True,
    ) -> None:
        super().__init__(data, period_config, memory, retention, init)
        if self._init:
            self.init()

    def init(self):
        high = self._data["high"].to_numpy(np.float64)
        low = self._data["low"].to_numpy(np.float64)
        close = self._data["close"].to_numpy(np.float64)

        close_p = np.zeros(close.size, dtype=np.float64)
        tr = np.zeros(close.size, dtype=np.float64)

        tr, tr_latest, close_p = _tr(high, low, close, close_p, tr)

        # Save numpy copy for indicators that depend on tr
        self._tr = tr

        # If memory set, convert to array
        if self._memory:
            self._tr = array("d", tr)

        self._tr_latest = tr_latest
        self._close_p = close_p

        self.drop_data()

    def update(self, data: pd.Series) -> np.float64:
        high = data["high"]
        low = data["low"]
        close = data["close"]

        self._tr_latest = _tr_update(high, low, self._close_p)

        if self._memory:
            self._tr.append(self._tr_latest)

        self._close_p = close
        return self._tr_latest

    def to_array(self, get: Literal["tr"] = "tr"):
        return super().to_array(get)

    def to_numpy(
        self,
        get: Literal["tr"] = "tr",
        dtype: np.dtype | None = np.float64,
        **kwargs,
    ):
        return super().to_numpy(get, dtype, **kwargs)

    def to_series(
        self,
        get: Literal["tr"] = "tr",
        dtype: type | None = float,
        name: str | None = None,
        **kwargs,
    ):
        return super().to_series(get, dtype, name, **kwargs)

    def tr_latest(self):
        return self._tr_latest
