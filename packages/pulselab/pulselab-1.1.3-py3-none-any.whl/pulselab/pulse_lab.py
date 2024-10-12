# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:05:29 2020

functions that support the generation of pulsed waveforms targeted at the 
M8195A

@author: gumcbrid
"""

import numpy as np
from scipy import signal
from scipy import io as sio
from collections import namedtuple as namedtuple

Waveform = namedtuple("Waveform", "wave, timebase")


def timebase(start, stop, sample_rate):
    start_sample = int(start * sample_rate)
    stop_sample = int(stop * sample_rate)
    timebase = np.arange(start_sample, stop_sample)
    timebase = timebase / sample_rate
    return timebase


def filterWave(sampleRate, bandwidth, wave):
    dx = 1 / sampleRate
    sigma = 0.3 / bandwidth
    gx = np.arange(-3 * sigma, 3 * sigma, dx)
    gaussian = np.exp(-((gx / sigma) ** 2) / 2)
    filtered = signal.fftconvolve(wave, gaussian, mode="full") / np.sum(gaussian)
    filtered = filtered[(int(len(gaussian) / 2)) : (-1 * int(len(gaussian) / 2)) + 1]
    return filtered


def createIdealPulseTrain(sampleRate, pulseWidth, repRate, pulseTrain):
    # Create a window of samples based on the PRI. This is a ' 10x super sampled'
    # timebase to allow more accurate edge placement. It is later downsampled
    # to the actual sample rate of the AWG
    superRate = 10 * sampleRate
    t = timebase(0, repRate * len(pulseTrain), superRate)
    wave = np.full(len(t), 0.0, dtype=float)
    for pulse in range(len(pulseTrain)):
        if pulseTrain[pulse] == 1:
            start = int(pulse * repRate * superRate)
            end = int(start + pulseWidth * superRate)
            wave[start:end] = 1.0
    return wave


def createPulseTrain(sampleRate, pulseWidth, repRate, pulseTrain, bandwidth):
    wave = createIdealPulseTrain(sampleRate, pulseWidth, repRate, pulseTrain)
    filteredWave = filterWave(sampleRate, bandwidth, wave)
    awgWave = signal.decimate(filteredWave, 10)
    t = timebase(0, len(awgWave) / sampleRate, sampleRate)
    return Waveform(awgWave, t)


def createPulse(
    sampleRate: float,
    pulseWidth: float,
    bandwidth: float,
    amplitude: float = 1,
    offset: float = 0,
    carrier: float = 0.0,
    phase: float = 0,
    precision: int = 10,
):
    """Creates an array of voltages representing the pulse shape against time
    Parameters:
    sampleRate: Typically the sample rate of the AWG (sa/s).
    pulseWidth: The nominal width of the pulse (s).
    bandwidth: The pulse shaping filter bandwith (Hz).
    amplitude: Relative to other pulses amplitude (0.0 - 1.0)
    carrier: Carrier frequency inside pulse (Hz).
    phase: Carrier phase (degrees).
    precision: Timing of envelope precision multiplier of sampleRate
    Returns:
    wave: the array of voltage samples.
    timebase: the timestamps associated with wave.
    """
    superRate = sampleRate * precision
    leadIn = 1 / bandwidth
    leadInSamples = int(np.ceil(leadIn * superRate))
    leadOutSamples = leadInSamples

    wave = np.concatenate(
        [np.zeros(leadInSamples), np.ones(int(pulseWidth * superRate)), np.zeros(leadOutSamples)]
    )
    t = np.arange(0, len(wave))
    t = t / superRate + (offset - leadIn)
    filteredWave = filterWave(superRate, bandwidth, wave)
    awgWave = signal.decimate(filteredWave, precision)
    timebase = np.arange(0, len(awgWave))
    timebase = timebase / sampleRate + t[0]
    awgWave = awgWave * amplitude
    rf = createTone(carrier, phase, timebase)
    awgWave = awgWave * amplitude * rf
    return Waveform(awgWave.astype(complex), timebase)


def createTone(frequency, phase, timebase):
    imag = np.sin((frequency * 2 * np.pi * timebase) + (phase * np.pi / 180))
    real = np.cos((frequency * 2 * np.pi * timebase) + (phase * np.pi / 180))
    wave = real + 1j * imag
    return wave


def createCsv(sampleRate, filename, wave):
    rpts = int(np.lcm(len(wave), 128) / len(wave))
    f = open(filename, "w")
    f.write("SampleRate={}\n".format(int(sampleRate)))
    f.write("SetConfig=true\n")
    f.write("Y1\n")
    for sample in np.tile(wave, rpts):
        f.write("{}\n".format(sample))
    f.close()


def createMat(sampleRate, filename, wave):
    rpts = int(np.lcm(len(wave), 128) / len(wave))
    XDelta = 1 / sampleRate

    matparams = {"InputZoom": [[1]], "XDelta": XDelta, "XStart": [[0]], "Y": np.tile(wave, rpts)}
    sio.savemat(filename, matparams)


######################################################
# MAIN!!!!!
######################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    SAMPLE_RATE = 1e09
    SYSTEM_BANDWIDTH = 200e06

    WIDTH = 5e-9
    PRI = 1000e-9
    AMPLITUDE = 0.5
    PULSE_TRAIN = [
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        0,
    ]  # Relative to time = 0. We need some lead-in time for the pulse shaping

    waveform = createPulseTrain(SAMPLE_RATE, WIDTH, PRI, PULSE_TRAIN, SYSTEM_BANDWIDTH)
    wave = waveform.wave
    t = waveform.timebase
    #    tone = createTone(SAMPLE_RATE, 10E6, 0, t)
    #   rfWave = wave * tone

    #    pulse = createPulse(SAMPLE_RATE, WIDTH, SYSTEM_BANDWIDTH, AMPLITUDE)

    plt.plot(t, wave)
    #    plt.plot(t, rfWave)
    plt.show()

#    plt.plot(pulse.timebase, pulse.wave)
