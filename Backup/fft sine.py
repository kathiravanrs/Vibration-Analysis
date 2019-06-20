from cmath import pi, exp
from math import log2, ceil
from bokeh.plotting import figure, show, output_file
import numpy as np


def nxt_power_2(x):
    return 2**ceil(log2(x))


def zero_padding(array):
    nextpwr = nxt_power_2(len(array))
    length_of_array = len(array)
    if nextpwr != length_of_array:
        for j in range(nextpwr-length_of_array):
            array.append(0)


def fft(x):
    n = len(x)
    if n <= 1:
        return x
    even_terms = fft(x[0::2])
    odd_terms = fft(x[1::2])
    t = [exp(-2j * pi * k / n) * odd_terms[k] for k in range(n // 2)]
    return [even_terms[k] + t[k] for k in range(n // 2)] +\
           [even_terms[k] - t[k] for k in range(n // 2)]


Fs = 1024.0
Ts = 1.0/Fs
time_range = np.arange(0, 1, Ts)
y = 6 * np.sin(2 * np.pi * 50 * time_range) + 5 * np.cos(2 * np.pi * 100 * time_range) + \
    4 * np.sin(2 * np.pi * 250 * time_range) + 3 * np.cos(2 * np.pi * 175 * time_range) + \
    10 * np.random.normal(0.0, 0.5, 1024) + 5 * np.random.normal(0, 0.4, 1024)


length = len(y)
q = np.arange(length)
time = length / Fs
frq = q / time
frq = frq[range(length // 2)]


Y = fft(y)
Y = Y[:len(Y)//2]


output_file("Graph/Sine Fourier.html")
plot = figure(title="sine fourier", plot_width=1500, plot_height=700)
plot.line(frq, [abs(y)/len(Y) for y in Y])
show(plot)

output_file("Graph/Sine.html")
plot = figure(title="sine", plot_width=1500, plot_height=700)
plot.line(time_range, y)
show(plot)
