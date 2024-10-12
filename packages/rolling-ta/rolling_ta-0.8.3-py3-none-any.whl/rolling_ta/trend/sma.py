from array import array
from typing import Literal

import numpy as np
import pandas as pd

from rolling_ta.extras.numba import _sma, _sma_update
from rolling_ta.indicator import Indicator


class SMA(Indicator):
    """
    A class to represent the Simple Moving Average (SMA) indicator.

    The SMA calculates the average of a selected range of prices by the number of periods in that range.
    It smooths out price data to help identify trends over time. This class computes the SMA using historical
    price data over a specified period.

    Material
    --------
        https://www.investopedia.com/terms/s/sma.asp
        https://pypi.org/project/ta/
    """

    _sma_latest = np.nan

    def __init__(
        self,
        data: pd.DataFrame,
        period_config: int = 14,
        memory: bool = True,
        retention: int = 20000,
        init: bool = True,
    ) -> None:
        super().__init__(data, period_config, memory, retention, init)
        if init:
            self.init()

    def init(self):
        close = self._data["close"].to_numpy(dtype=np.float64)
        sma = np.zeros(close.size)

        sma, window, window_sum, latest = _sma(close, sma, self._period_config)

        self._window = window
        self._window_sum = window_sum
        self._sma_latest = latest

        if self._memory:
            self._sma = array("f", sma)

        self.drop_data()
        self.set_initialized()

    def update(self, data: pd.Series):

        latest, window, window_sum = _sma_update(
            data["close"],
            self._window_sum,
            self._window,
            self._period_config,
        )

        self._sma_latest = latest
        self._window_sum = window_sum
        self._window = window

        if self._memory:
            self._sma.append(latest)

    def sma_latest(self):
        return self._sma_latest

    def to_array(self, get: Literal["sma"] = "sma"):
        return super().to_array(get)

    def to_numpy(
        self,
        get: Literal["sma"] = "sma",
        dtype: np.dtype | None = np.float64,
        **kwargs,
    ):
        return super().to_numpy(get, dtype, **kwargs)

    def to_series(
        self,
        get: Literal["sma"] = "sma",
        dtype: type | None = float,
        name: str | None = None,
        **kwargs,
    ):
        return super().to_series(get, dtype, name, **kwargs)
