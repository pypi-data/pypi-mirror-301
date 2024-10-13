from typing import Tuple

import numpy as np


class AawareForwardTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 1,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns') -> None:
        import pyaaware

        self._ft = pyaaware._ForwardTransform()
        self._config = self._ft.config()

        self._config.N = N
        self._config.R = R
        self._config.bin_start = bin_start
        self._config.bin_end = bin_end
        self._config.ttype = ttype
        self._device = 'cpu'

        self._ft.config(self._config, False)
        self._config = self._ft.config()
        self._bins = self._config.bin_end - self._config.bin_start + 1

    @property
    def N(self) -> int:
        return self._config.N

    @property
    def R(self) -> int:
        return self._config.R

    @property
    def bin_start(self) -> int:
        return self._config.bin_start

    @property
    def bin_end(self) -> int:
        return self._config.bin_end

    @property
    def ttype(self) -> str:
        return self._config.ttype

    @property
    def device(self) -> str:
        return self._device

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def W(self) -> np.ndarray:
        return self._ft.W()

    def reset(self) -> None:
        self._ft.reset()

    def execute_all(self, xt: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute the multichannel, forward FFT of the time domain input.

        :param xt: Numpy array of time domain data with dimensions [batch, samples]
        :return: Tuple containing frequency domain frame data and frame-based energy data
            yf: [batch, frames, bins]
            energy_t: [batch, frames]
        """
        if xt.ndim != 1 and xt.ndim != 2:
            raise ValueError('Input must have 1 or 2 dimensions')

        no_batch = xt.ndim == 1
        if no_batch:
            batches = 1
            samples = xt.shape[0]
        else:
            batches, samples = xt.shape

        frames = (samples + self.R - 1) // self.R
        extra_samples = frames * self.R - samples

        if no_batch:
            xt_pad = np.pad(array=xt,
                            pad_width=(0, extra_samples),
                            mode='constant',
                            constant_values=0)
        else:
            xt_pad = np.pad(array=xt,
                            pad_width=((0, extra_samples), (0, 0)),
                            mode='constant',
                            constant_values=0)

        yf = np.empty((batches, frames, self.bins), dtype=np.complex64)
        energy_t = np.empty((batches, frames), dtype=np.float32)

        for batch in range(batches):
            for frame in range(frames):
                start = frame * self.R
                stop = start + self.R
                tmp = np.empty(self.bins, dtype=np.complex64)
                if no_batch:
                    self._ft.execute(xt_pad[start:stop], tmp)
                else:
                    self._ft.execute(xt_pad[batch, start:stop], tmp)
                yf[batch, frame, :] = tmp
                energy_t[batch, frame] = self._ft.energy_t()
            self.reset()

        if no_batch:
            yf = yf.squeeze()
            energy_t = energy_t.squeeze()

        return yf, energy_t

    def execute(self, xt: np.ndarray) -> Tuple[np.ndarray, np.float32]:
        """Compute the forward FFT of the time domain input.

        :param xt: Numpy array of time domain data with dimensions [samples]
        :return: Tuple containing frequency domain frame data and frame-based energy data
            yf: [bins]
            energy_t: scalar
        """
        if xt.ndim != 1:
            raise ValueError('Input must have 1 dimensions [bins]')

        if xt.shape[0] != self.R:
            raise ValueError(f'Input must have {self.R} samples')

        yf = np.empty(self.bins, dtype=np.complex64)
        self._ft.execute(xt, yf)
        energy_t = self._ft.energy_t()
        return yf, energy_t
