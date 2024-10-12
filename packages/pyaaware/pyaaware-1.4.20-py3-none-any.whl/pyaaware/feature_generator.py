from typing import Optional
from typing import Tuple

import numpy as np


class FeatureGenerator:
    def __init__(self,
                 feature_mode: Optional[str] = None,
                 num_classes: Optional[int] = None,
                 truth_mutex: Optional[bool] = None) -> None:
        import pyaaware

        self._fg = pyaaware._FeatureGenerator()
        self._config = self._fg.config()

        if feature_mode is not None:
            self._config.feature_mode = feature_mode

        if num_classes is not None:
            self._config.num_classes = num_classes

        if truth_mutex is not None:
            self._config.truth_mutex = 1 if truth_mutex else 0

        self._fg.config(self._config)
        self._bins = self._fg.bin_end() - self._fg.bin_start() + 1

    @property
    def frame_size(self) -> int:
        return self._config.frame_size

    @property
    def feature_mode(self) -> str:
        return self._config.feature_mode

    @property
    def num_classes(self) -> int:
        return self._config.num_classes

    @property
    def truth_mutex(self) -> bool:
        return self._config.truth_mutex != 0

    @property
    def use_history(self) -> bool:
        return self._config.use_history != 0

    @property
    def bin_start(self) -> int:
        return self._fg.bin_start()

    @property
    def bin_end(self) -> int:
        return self._fg.bin_end()

    @property
    def num_bands(self) -> int:
        return self._fg.num_bands()

    @property
    def stride(self) -> int:
        return self._fg.stride()

    @property
    def step(self) -> int:
        return self._fg.step()

    @property
    def decimation(self) -> int:
        return self._fg.decimation()

    @property
    def feature_size(self) -> int:
        return self._fg.feature_size()

    @property
    def ftransform_N(self) -> int:
        return self._fg.ftransform_N()

    @property
    def ftransform_R(self) -> int:
        return self._fg.ftransform_R()

    @property
    def ftransform_ttype(self) -> str:
        return self._fg.ftransform_ttype()

    @property
    def eftransform_N(self) -> int:
        return self._fg.eftransform_N()

    @property
    def eftransform_R(self) -> int:
        return self._fg.eftransform_R()

    @property
    def eftransform_ttype(self) -> str:
        return self._fg.eftransform_ttype()

    @property
    def itransform_N(self) -> int:
        return self._fg.itransform_N()

    @property
    def itransform_R(self) -> int:
        return self._fg.itransform_R()

    @property
    def itransform_ttype(self) -> str:
        return self._fg.itransform_ttype()

    def reset(self) -> None:
        self._fg.reset()

    def execute_all(self, xf: np.ndarray, truth_in: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        assert xf.ndim == 3 or xf.ndim == 2

        has_channels = xf.ndim == 3
        if has_channels:
            channels = xf.shape[0]
            input_frames = xf.shape[1]
            bins = xf.shape[2]
        else:
            channels = 1
            input_frames = xf.shape[0]
            bins = xf.shape[1]

        assert bins == self._bins

        if truth_in is not None:
            assert truth_in.ndim == xf.ndim
            if has_channels:
                assert truth_in.shape[0] == channels
                assert truth_in.shape[1] == input_frames
                assert truth_in.shape[2] == self.num_classes
            else:
                assert truth_in.shape[0] == input_frames
                assert truth_in.shape[1] == self.num_classes

        output_frames = int(input_frames / (self.step * self.decimation))

        if has_channels:
            feature = np.empty((channels, output_frames, self.stride, self.num_bands), dtype=np.float32)
            truth = np.empty((channels, output_frames, self.num_classes), dtype=np.complex64)
        else:
            feature = np.empty((output_frames, self.stride, self.num_bands), dtype=np.float32)
            truth = np.empty((output_frames, self.num_classes), dtype=np.complex64)

        for channel in range(channels):
            output_frame = 0
            for input_frame in range(input_frames):
                if truth_in is not None:
                    if has_channels:
                        self._fg.execute(xf[channel, input_frame], truth_in[channel, input_frame])
                    else:
                        self._fg.execute(xf[input_frame], truth_in[input_frame])
                else:
                    if has_channels:
                        self._fg.execute(xf[channel, input_frame])
                    else:
                        self._fg.execute(xf[input_frame])

                if self._fg.eof():
                    if has_channels:
                        feature[channel, output_frame] = self._fg.feature()
                        truth[channel, output_frame] = self._fg.truth()
                    else:
                        feature[output_frame] = self._fg.feature()
                        truth[output_frame] = self._fg.truth()
                    output_frame += 1

        return feature, truth

    def execute(self, xf: np.ndarray, truth_in: Optional[np.ndarray] = None) -> None:
        assert xf.ndim == 1

        bins = xf.shape[-1]
        assert bins == self._bins

        if truth_in is not None:
            assert truth_in.ndim == 1
            assert truth_in.shape[-1] == self.num_classes

        if truth_in is not None:
            self._fg.execute(xf, truth_in)
        else:
            self._fg.execute(xf)

    def eof(self) -> bool:
        return self._fg.eof()

    def feature(self) -> np.ndarray:
        return self._fg.feature()

    def truth(self) -> np.ndarray:
        return self._fg.truth()
