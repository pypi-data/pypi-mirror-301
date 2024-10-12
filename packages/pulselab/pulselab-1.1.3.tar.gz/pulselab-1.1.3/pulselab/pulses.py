from copy import deepcopy
import numpy as np
from .pulse import Pulse

def __dir__():
    return [Pulses]

class Pulses:

    def __init__(
        self,
        base_descriptor: Pulse,
        pri: float,
        count: int,
    ):
        self._pdt = [deepcopy(base_descriptor) for i in range(count)]
        self.pri = pri
        self.count = count
        self._wave = None
        self._timebase = None
        delay = self._pdt[0].delay
        for pd in self._pdt:
            pd.delay = delay
            delay += pri

    @property
    def pdt(self):
        return self._pdt

    @property
    def wave(self):
        self._build_wave()
        return self._wave

    @property
    def timebase(self):
        self._build_wave()
        return self._timebase

    def increasing_width(self, increment):
        width = self._pdt[0].width
        for pd in self._pdt:
            pd.width = width
            width += increment

    def increasing_phase(self, increment):
        phase = self._pdt[0].phase
        for pd in self._pdt:
            pd.phase = phase
            phase += increment

    def increasing_carrier(self, increment):
        carrier = self._pdt[0].carrier
        for pd in self._pdt:
            pd.carrier = carrier
            carrier += increment

    def increasing_delay(self, increment):
        delay = increment
        for pd in self._pdt:
            pd.delay += delay
            delay += increment

    def _build_wave(self):
        samples_per_wave = round(self.pri * self.count * Pulse.sample_rate)  # This needs modifying to account for increasing delay scenario
        self._wave = np.zeros(samples_per_wave, dtype=complex)
        self._timebase = np.arange(0, len(self._wave)) / Pulse.sample_rate
        for pulse in self._pdt:
            self._wave[pulse.sample_first : pulse.sample_last] += pulse.wave
