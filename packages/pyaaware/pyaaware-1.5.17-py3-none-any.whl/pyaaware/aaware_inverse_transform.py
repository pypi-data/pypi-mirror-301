from typing import Tuple

import numpy as np

import pyaaware


class AawareInverseTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 1,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns',
                 gain: np.float32 = 1,
                 trim: bool = True) -> None:
        self._it = pyaaware._InverseTransform()
        self._config = self._it.config()

        self._config.N = N
        self._config.R = R
        self._config.bin_start = bin_start
        self._config.bin_end = bin_end
        self._config.ttype = ttype
        self._config.gain = gain

        self._padding_needed = self.ttype not in ('stft-ols', 'stft-ola')
        if self._padding_needed:
            self._trim = trim
        else:
            self._trim = False

        self._config.trim = self._trim

        self._it.config(self._config, False)
        self._config = self._it.config()
        self._bins = self._config.bin_end - self._config.bin_start + 1
        self._device = 'cpu'

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
    def gain(self) -> np.float32:
        return self._config.gain

    @property
    def trim(self) -> bool:
        return self._trim

    @property
    def device(self) -> str:
        return self._device

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def W(self) -> np.ndarray:
        return self._it.W()

    def reset(self) -> None:
        self._it.reset()

    def execute_all(self, xf: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute the multichannel, real, inverse FFT of the frequency domain input.

        :param xf: Numpy array of frequency domain data with dimensions [batch, frames, bins]
        :return: Tuple containing time domain sample data and frame-based energy data
            yt: [batch, samples]
            energy_t: [batch, frames]
        """
        if xf.ndim != 2 and xf.ndim != 3:
            raise ValueError('Input must have 2 dimensions [frames, bins] or 3 dimensions [batch, frames, bins]')

        no_batch = xf.ndim == 2

        if self._padding_needed:
            padding_samples = self.N - self.R
            padding_frames = padding_samples // self.R
            if no_batch:
                xf = np.pad(xf, ((0, padding_frames), (0, 0)), mode='constant', constant_values=0)
            else:
                xf = np.pad(xf, ((0, 0), (0, padding_frames), (0, 0)), mode='constant', constant_values=0)
        else:
            padding_samples = 0
            padding_frames = 0

        if no_batch:
            batches = 1
            frames, bins = xf.shape
        else:
            batches, frames, bins = xf.shape

        if bins != self.bins:
            raise ValueError(f'Input must have {self.bins} bins [batch, frames, bins]')

        samples = frames * self.R

        yt = np.empty((batches, samples), dtype=np.float32)
        energy_t = np.empty((batches, frames), dtype=np.float32)

        for batch in range(batches):
            for frame in range(frames):
                start = frame * self.R
                stop = start + self.R
                tmp = np.empty(self.R, dtype=np.float32)
                if no_batch:
                    self._it.execute(xf[frame, :], tmp)
                else:
                    self._it.execute(xf[batch, frame, :], tmp)
                yt[batch, start:stop] = tmp
                energy_t[batch, frame] = self._it.energy_t()
            self.reset()

        if self.trim:
            yt = yt[..., padding_samples:]
            energy_t = energy_t[..., padding_frames:]

        if no_batch:
            yt = yt.squeeze()
            energy_t = energy_t.squeeze()

        return yt, energy_t

    def execute(self, xf: np.ndarray) -> Tuple[np.ndarray, np.float32]:
        """Compute the real, inverse FFT of the frequency domain input.

        :param xf: Numpy array of frequency domain data with dimensions [bins]
        :return: Tuple containing time domain sample data and frame-based energy data
            yt: [samples]
            energy_t: [frames]
        """
        if xf.ndim != 1:
            raise ValueError('Input must have 1 dimensions [bins]')

        if xf.shape[0] != self.bins:
            raise ValueError(f'Input must have {self.bins} bins')

        yt = np.empty(self.R, dtype=np.float32)
        self._it.execute(xf, yt)
        energy_t = self._it.energy_t()
        return yt, energy_t
