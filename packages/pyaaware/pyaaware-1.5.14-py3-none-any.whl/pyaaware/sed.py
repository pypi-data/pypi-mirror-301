from typing import List
from typing import Optional

import numpy as np


class SED:
    def __init__(self,
                 thresholds: Optional[List[np.float32]] = None,
                 index: Optional[List[int]] = None,
                 frame_size: Optional[int] = None,
                 num_classes: Optional[int] = None,
                 mutex: Optional[bool] = None) -> None:
        import pyaaware

        self._sed = pyaaware._SED()
        self._config = self._sed.config()

        if thresholds is not None:
            self._config.thresholds = thresholds

        if index is not None:
            self._config.index = index

        if frame_size is not None:
            self._config.frame_size = frame_size

        if num_classes is not None:
            self._config.num_classes = num_classes

        if mutex is not None:
            self._config.mutex = 1 if mutex else 0

        self._sed.config(self._config)

    @property
    def thresholds(self) -> List[int]:
        return self._config.thresholds

    @property
    def index(self) -> List[int]:
        return self._config.index

    @property
    def frame_size(self) -> int:
        return self._config.frame_size

    @property
    def num_classes(self) -> int:
        return self._config.num_classes

    @property
    def mutex(self) -> int:
        return self._config.mutex != 0

    def reset(self):
        self._sed.reset()

    def execute_all(self, x: np.ndarray) -> np.ndarray:
        y = np.empty((self.num_classes, x.shape[0]), dtype=np.float32)
        for in_idx in range(len(x)):
            y[:, in_idx] = self._sed.execute(x[in_idx])

        return y

    def execute(self, x: float) -> np.ndarray:
        return self._sed.execute(x)
