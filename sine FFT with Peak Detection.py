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


def find_peaks(arr):
    peak_indices = []
    mean = sum(arr)/len(arr)
    for i in range(1, len(arr)-1):
        if arr[i-1] < arr[i] > arr[i+1] and arr[i] > mean:
            peak_indices.append(i)
    return peak_indices


def peak_pos(indices, y_axis, x_axis):
    position = []
    for i in indices:
        position.append((x_axis[i], y_axis[i]))
    return position


Fs = 1024.0
Ts = 1.0/Fs
time_range = np.arange(0, 1, Ts)
y = 6 * np.sin(2 * np.pi * 50 * time_range) + 9 * np.cos(2 * np.pi * 100 * time_range) + \
    7 * np.sin(2 * np.pi * 250 * time_range) + 3 * np.cos(2 * np.pi * 175 * time_range) + \
    7 * np.random.normal(0.0, 0.5, 1024) + 7 * np.random.normal(0, 0.4, 1024)


length = len(y)
q = np.arange(length)
time = length / Fs
frq = q / time
frq = frq[range(length // 2)]


Y = fft(y)
Y = Y[:len(Y)//2]

power = [(abs(y)/len(Y))**2 for y in Y]
normalisedFourier = [abs(y)/len(Y) for y in Y]

print(sum(power)/len(power))

output_file("Graph/Sine Fourier power.html")
plot = figure(title="sine fourier", plot_width=1500, plot_height=700)
plot.line(frq, power)
show(plot)

output_file("Graph/Sine Fourier.html")
plot = figure(title="sine fourier", plot_width=1500, plot_height=700)
plot.line(frq, normalisedFourier)
show(plot)

output_file("Graph/Sine.html")
plot = figure(title="sine", plot_width=1500, plot_height=700)
plot.line(time_range, y)
show(plot)

index = find_peaks(power)
print(index)
print(peak_pos(index, power, frq))
