import torch


class TorchInverseTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 1,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns',
                 gain: torch.float32 = 1,
                 trim: bool = True) -> None:
        import numpy as np

        from pyaaware.transform_types import Overlap
        from pyaaware.transform_types import Window
        from pyaaware.transform_types import window

        self._N = N
        self._R = R
        self._bin_start = bin_start
        self._bin_end = bin_end
        self._ttype = ttype
        self._gain = gain

        # Note: init is always on CPU; will move if needed in execute_all() or execute()
        self._device = 'cpu'

        if self.N % self.R:
            raise ValueError('R is not a factor of N')

        if self.bin_start >= self.N:
            raise ValueError('bin_start is greater than N')

        if self.bin_end >= self.N:
            raise ValueError('bin_end is greater than N')

        if self.bin_start >= self.bin_end:
            raise ValueError('bin_start is greater than bin_end')

        self._real_mode = self.bin_end <= self.N // 2
        self._cj_indices = list(range(self.N // 2 + 1, self.N))
        self._i_indices = list(range((self.N + 1) // 2 - 1, 0, -1))
        self._ob_indices = list(range(self.N - self.R, self.N))
        self._bin_indices = list(range(self.bin_start, self.bin_end + 1))
        self._bins = self.bin_end - self.bin_start + 1

        self._W = None
        self._overlap_type = None
        self._xfs = None
        self._pyo = None
        self._padding_needed = True

        if self.ttype == 'stft-olsa-hanns':
            self._W = window(Window.HANN01, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-ols':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N ** 2 / self.R / 2
            self._overlap_type = Overlap.OLS
            self._padding_needed = False
        elif self.ttype == 'stft-olsa':
            self._W = window(Window.W01, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hann':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hannd':
            self._W = window(Window.HANN, self.N, self.R)
            itr_user_gain = self.N / 3
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hammd':
            self._W = window(Window.HAMM, self.N, self.R)
            itr_user_gain = self.N / 2.72565243
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-ola':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N ** 2 / self.R / 2
            self._overlap_type = Overlap.OLA
            self._padding_needed = False
        elif self.ttype in ('tdac', 'tdac-co'):
            self._R = self.N // 2
            self._real_mode = False

            k = torch.arange(1, self.R)
            self._W = torch.conj(torch.exp(-1j * 2 * torch.pi / 8 * (2 * k + 1)) * torch.exp(
                -1j * 2 * torch.pi / (2 * self.N) * k)) / 4
            itr_user_gain = 1

            if self.ttype == 'tdac':
                self._overlap_type = Overlap.TDAC
            else:
                self._overlap_type = Overlap.TDAC_CO
        else:
            raise ValueError(f"Unknown ttype: '{self.ttype}'")

        if self._overlap_type not in (Overlap.TDAC, Overlap.TDAC_CO):
            if len(self.W) != self.N:
                raise RuntimeError('W is not of length N')

            wdc_gain = torch.sum(self.W)
            o_gain = 1 / (self.gain * wdc_gain / self.R) * itr_user_gain
            self._W = self.W * o_gain

        # Check if in sub-bin mode (feature not full bin, thus are zeroed out for transforms)
        if self._ttype in ('tdac', 'tdac-co'):
            self._partial_bin = self._bin_start > 0 or self._bin_end < self.N // 2 - 1
            # Full TDAC has bins 0:floor(N/2)-1, must be even
            self._last_full_bin = self.N // 2 - 1
        else:
            self._partial_bin = self._bin_start > 0 or self._bin_end < self.N // 2
            # Full FFT has bins 0:floor(N/2)
            self._last_full_bin = self.N // 2

        self.fold_params = {
            'kernel_size': (self.N, 1),
            'stride':      (self.R, 1),
        }

        if self._padding_needed:
            self._trim = trim
        else:
            self._trim = False

        self._sqrt_N = np.sqrt(self.N)
        self._sqrt_eighth = np.sqrt(1 / 8)
        self.reset()

    @property
    def N(self) -> int:
        return self._N

    @property
    def R(self) -> int:
        return self._R

    @property
    def bin_start(self) -> int:
        return self._bin_start

    @property
    def bin_end(self) -> int:
        return self._bin_end

    @property
    def ttype(self) -> str:
        return self._ttype

    @property
    def gain(self) -> torch.float32:
        return self._gain

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
    def W(self) -> torch.Tensor:
        return self._W

    def reset(self) -> None:
        self._xfs = torch.zeros(self.N, dtype=torch.complex64, device=self.device)
        self._pyo = torch.zeros(self.N, dtype=torch.float32, device=self.device)

    def _check_device(self, xf: torch.Tensor) -> None:
        if xf.device != self.device:
            self._device = xf.device
            self._W = self.W.to(self.device)
            self._pyo = self._pyo.to(self.device)
            self._xfs = self._xfs.to(self.device)

    def execute_all(self, xf: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute the multichannel, real, inverse FFT of the frequency domain input.

        :param xf: Tensor of frequency domain data with dimensions [batch, frames, bins]
        :return: Tuple containing time domain sample data and frame-based energy data
            yt: [batch, samples]
            energy_t: [batch, frames]
        """
        from pyaaware.transform_types import Overlap

        if xf.ndim != 2 and xf.ndim != 3:
            raise ValueError('Input must have 2 dimensions [frames, bins] or 3 dimensions [batch, frames, bins]')

        self._check_device(xf)

        no_batch = xf.ndim == 2

        if self._padding_needed:
            padding_samples = self.N - self.R
            padding_frames = padding_samples // self.R
        else:
            padding_samples = 0
            padding_frames = padding_samples // self.R

        xf_pad = torch.nn.functional.pad(xf, (0, 0, 0, padding_frames), mode='constant', value=0)
        if no_batch:
            batch = 1
            frames, bins = xf_pad.shape
        else:
            batch, frames, bins = xf_pad.shape

        if bins != self.bins:
            raise ValueError(f'Input must have {self.bins} bins [batch, frames, bins]')

        samples = frames * self.R

        if self._partial_bin:
            if no_batch:
                zero = torch.zeros((frames, self._last_full_bin + 1), dtype=xf_pad.dtype, device=self.device)
            else:
                zero = torch.zeros((batch, frames, self._last_full_bin + 1), dtype=xf_pad.dtype, device=self.device)
            # TODO: may need to use clone to keep gradients correct
            zero[..., self._bin_indices] = xf_pad
            xf_pad = zero

        if self._overlap_type == Overlap.OLA:
            # Multichannel, real, inverse FFT, norm='backward' normalizes by 1/n
            yt = torch.fft.irfft(xf_pad, dim=-1, n=self.N, norm='backward')

            # multichannel window, torch.tensor expands over [batch, frames]
            if no_batch:
                yt = yt * self.W.view(1, -1)
            else:
                yt = yt * self.W.view(1, 1, -1)

            # Use nn.fold() to apply overlap-add
            if no_batch:
                yt = yt.permute(1, 0)
            else:
                yt = yt.permute(0, 2, 1)
            expected_output_signal_len = self.N + self.R * (frames - 1)
            yt = torch.nn.functional.fold(yt, output_size=(expected_output_signal_len, 1), **self.fold_params)
            if no_batch:
                yt = yt.reshape(-1)
                yt = yt[:samples]
            else:
                yt = yt.reshape(yt.shape[0], -1)
                yt = yt[:, :samples]

        elif self._overlap_type == Overlap.OLS:
            # Multichannel, real, inverse FFT, norm='backward' normalizes by 1/n
            yt = torch.fft.irfft(xf_pad, dim=-1, n=self.N, norm='backward')

            # Multichannel window, torch.tensor expands over [batch, frames]
            if no_batch:
                yt = yt * self.W.view(1, -1)
                yt = yt[:, self._ob_indices]
                yt = yt.reshape(-1)
            else:
                yt = yt * self.W.view(1, 1, -1)
                yt = yt[:, :, self._ob_indices]
                yt = yt.reshape(yt.shape[0], -1)

        elif self._overlap_type in (Overlap.TDAC, Overlap.TDAC_CO):
            # Create buffer for complex input to real inverse FFT which wants [batch, frames, N//2+1]
            # note xf_pad already expanded to full-bin, but TDAC full-bin is always one less, i.e. N//2
            if no_batch:
                tdx = torch.zeros((frames, self.R + 1), dtype=xf_pad.dtype, device=self.device)
            else:
                tdx = torch.zeros((batch, frames, self.R + 1), dtype=xf_pad.dtype, device=self.device)
            if self._overlap_type == Overlap.TDAC:
                if no_batch:
                    tdx[:, 1:self.R] = self.W.view(1, -1) * (
                            xf_pad[:, 0:self.R - 1] - 1j * xf_pad[:, 1:self.R])
                    tdx[:, 0] = self._sqrt_eighth * (xf_pad[:, 0].real + xf_pad[:, 0].imag)
                    tdx[:, self.R] = -self._sqrt_eighth * (
                            xf_pad[:, self._last_full_bin].real + xf_pad[:, self._last_full_bin].imag)
                else:
                    tdx[:, :, 1:self.R] = self.W.view(1, 1, -1) * (
                            xf_pad[:, :, 0:self.R - 1] - 1j * xf_pad[:, :, 1:self.R])
                    tdx[:, :, 0] = self._sqrt_eighth * (xf_pad[:, :, 0].real + xf_pad[:, :, 0].imag)
                    tdx[:, :, self.R] = -self._sqrt_eighth * (
                            xf_pad[:, :, self._last_full_bin].real + xf_pad[:, :, self._last_full_bin].imag)
            else:
                if no_batch:
                    tdx[:, 1:self.R] = 2 * self.W.view(1, -1) * (
                            xf_pad[:, 0:self.R - 1] - 1j * xf_pad[:, 1:self.R])
                    tdx[:, 0] = 2 * self._sqrt_eighth * xf_pad[:, 0].real
                    tdx[:, self.R] = -2 * self._sqrt_eighth * xf_pad[:, self._last_full_bin].real
                else:
                    tdx[:, :, 1:self.R] = 2 * self.W.view(1, 1, -1) * (
                            xf_pad[:, :, 0:self.R - 1] - 1j * xf_pad[:, :, 1:self.R])
                    tdx[:, :, 0] = 2 * self._sqrt_eighth * xf_pad[:, :, 0].real
                    tdx[:, :, self.R] = -2 * self._sqrt_eighth * xf_pad[:, :, self._last_full_bin].real
            xf_pad = tdx

            # Multichannel, real, inverse FFT, norm='ortho' normalizes by 1/sqrt(n)
            yt = torch.fft.irfft(xf_pad, dim=-1, n=self.N, norm='ortho')

            # Use nn.fold() to apply overlap-add
            if no_batch:
                yt = yt.permute(1, 0)
            else:
                yt = yt.permute(0, 2, 1)
            expected_output_signal_len = self.N + self.R * (frames - 1)
            yt = torch.nn.functional.fold(yt, output_size=(expected_output_signal_len, 1), **self.fold_params)
            if no_batch:
                yt = yt.reshape(-1)
                yt = yt[:samples]
            else:
                yt = yt.reshape(yt.shape[0], -1)
                yt = yt[:, :samples]

        else:
            raise ValueError(f"Unsupported type: '{self.ttype}'")

        if self.trim:
            if no_batch:
                yt = yt[padding_samples:]
            else:
                yt = yt[:, padding_samples:]

        if no_batch:
            energy_t = torch.mean(torch.square(yt).reshape(-1, self.R), dim=-1)
        else:
            energy_t = torch.mean(torch.square(yt).reshape(yt.shape[0], -1, self.R), dim=-1)

        return yt, energy_t

    def execute(self, xf: torch.Tensor) -> tuple[torch.Tensor, float]:
        """Compute the real, inverse FFT of the frequency domain input.

        :param xf: Tensor of frequency domain data with dimensions [bins]
        :return: Tuple containing time domain sample data and frame-based energy data
            yt: [samples]
            energy_t: [frames]
        """
        from pyaaware.transform_types import Overlap

        if xf.ndim != 1:
            raise ValueError('Input must have 1 dimensions [bins]')

        if xf.shape[0] != self.bins:
            raise ValueError(f'Input must have {self.bins} bins')

        self._check_device(xf)

        self._xfs[self._bin_indices] = xf
        if self._real_mode:
            self._xfs[self._cj_indices] = torch.conj(self._xfs[self._i_indices])

        if not self.N % 2:
            self._xfs[self.N // 2].imag = 0

        if self._overlap_type == Overlap.OLA:
            tmp = self.W * torch.fft.irfft(self._xfs, n=self.N, norm='backward') + self._pyo
            self._pyo[0:(self.N - self.R)] = tmp[self.R:]
            yt = tmp[0:self.R]
        elif self._overlap_type == Overlap.OLS:
            tmp = self.W * torch.fft.irfft(self._xfs, n=self.N, norm='backward')
            yt = tmp[self._ob_indices]
        elif self._overlap_type in (Overlap.TDAC, Overlap.TDAC_CO):
            if self._overlap_type == Overlap.TDAC:
                self._xfs[self.N // 2] = -self._sqrt_eighth * (
                        self._xfs[self.N // 2 - 1].real + self._xfs[self.N // 2 - 1].imag)
                for n in range(self.N // 2 - 1, 0, -1):
                    self._xfs[n] = self.W[n - 1] * (self._xfs[n - 1] - 1j * self._xfs[n])
                self._xfs[0] = self._sqrt_eighth * (self._xfs[0].real + self._xfs[0].imag)
                for n in range(self.N // 2, self.N):
                    self._xfs[n] = torch.conj(self._xfs[self.N - n])
            else:
                self._xfs[self.N // 2] = -2 * self._sqrt_eighth * self._xfs[self.N // 2 - 1].real
                for n in range(self.N // 2 - 1, 0, -1):
                    self._xfs[n] = 2 * self.W[n - 1] * (self._xfs[n - 1] - 1j * self._xfs[n])
                self._xfs[0] = 2 * self._sqrt_eighth * self._xfs[0].real
                for n in range(self.N // 2, self.N):
                    self._xfs[n] = torch.conj(self._xfs[self.N - n])

            tmp = torch.real(torch.fft.irfft(self._xfs, n=self.N, norm='ortho')) + self._pyo
            self._pyo[0:(self.N - self.R)] = tmp[self.R:]
            yt = tmp[0:self.R]
        else:
            raise ValueError(f"Unsupported overlap type: '{self._overlap_type}'")

        energy_t = torch.mean(torch.square(yt))
        return yt, float(energy_t)
