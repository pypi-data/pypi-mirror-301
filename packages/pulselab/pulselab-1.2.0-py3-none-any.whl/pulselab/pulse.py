import numpy as np

from .pulse_lab import createPulse

def __dir__():
    return [Pulse]


class Pulse:

    sample_rate = None

    def __init__(
        self,
        carrier: float = 0.0,
        phase: float = 0.0,
        delay: float = 0.0,
        width: float = 0.0,
        bandwidth: float = float('nan'),
        amplitude: float = 1.0,
    ):
        self._carrier = carrier
        self._phase = phase % 360
        self._delay = delay
        self._width = width
        self._amplitude = amplitude
        if np.isnan(bandwidth):
            self._bandwidth = Pulse.sample_rate / 2
        else:
            self._bandwidth = bandwidth
        self._create_wave()

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = value
        self._create_wave()

    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        self._bandwidth = value
        self._create_wave()

    @property
    def carrier(self):
        return self._carrier

    @carrier.setter
    def carrier(self, value):
        self._carrier = value
        self._create_wave()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._create_wave()

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value
        self._create_wave()

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value % 360
        self._create_wave()

    @property
    def time_first(self):
        return self._time_first

    @property
    def sample_first(self):
        return round(self._time_first * Pulse.sample_rate) - 1

    @property
    def time_last(self):
        return self._time_last

    @property
    def sample_last(self):
        return self.sample_first + len(self.wave)

    @property
    def wave(self):
        return self._wave

    @property
    def timebase(self):
        return self._timebase

    def _create_wave(self):
        """Create a list of voltage points based on pulse descriptor
        Parameters:
        sample_rate: target sample rate of digitizer
        Returns:
        wave: list of voltage points scaled to 1.0
        """
        wave, t = createPulse(
            Pulse.sample_rate,
            self.width,
            self.bandwidth,
            self.amplitude,
            offset=self.delay,
            carrier=self.carrier,
            phase=self.phase,
        )
        self._time_first = t[0]
        self._time_last = t[-1]
        self._wave = wave
        self._timebase = t
