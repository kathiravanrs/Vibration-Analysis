import pandas as pd
from cmath import pi, exp
from math import log2, ceil
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d


def nxt_power_2(x):
    # Returns the nearest power of 2 larger than given number

    return 2**ceil(log2(x))


def zero_padding(array):

    # Adds a series of 0s to the end of signal until the signal length becomes a power of 2

    nextpwr = nxt_power_2(len(array))
    length_of_array = len(array)
    if nextpwr != length_of_array:
        for j in range(nextpwr-length_of_array):
            array.append(0)


def fft(x):
    # Calculates and returns the Discrete Fourier Transform using Cooley-Tukey's algorithm

    length = len(x)
    if length <= 1:
        return x
    even_terms = fft(x[0::2])
    odd_terms = fft(x[1::2])
    fourier = [exp(-2j * pi * p / length) * odd_terms[p] for p in range(length // 2)]
    return [even_terms[p] + fourier[p] for p in range(length // 2)] + \
           [even_terms[p] - fourier[p] for p in range(length // 2)]


input_data_path = "Data/Vibration Data.xlsx"
output_data_path = "Data/Fourier transformed Vibration Data.xlsx"
vibration_data = pd.read_excel(input_data_path)

# Separating the values of X and Y axis data
vibraX = pd.DataFrame(vibration_data, columns=['VibraX'])
vibraY = pd.DataFrame(vibration_data, columns=['VibraY'])

signal_length = len(vibraX)

vibraY = vibraY.values.tolist()
vibraX = vibraX.values.tolist()

sumx, sumy = 0, 0
for i in range(signal_length):
    sumy += vibraY[i][0]
    sumx += vibraX[i][0]

mean_x = sumx/signal_length
mean_y = sumy/signal_length

x_list, y_list = [], []
for i in range(signal_length):
    x_list.append(vibraX[i][0] - mean_x)
    y_list.append(vibraY[i][0] - mean_y)

zero_padding(x_list)
zero_padding(y_list)

Fs = 1                       # Sampling Frequency of the signal
n = len(x_list)              # Number of samples
k = [i for i in range(n)]
T = n/Fs                     # Total time = No of sample/Sample frequency
frq = [x / T for x in k]     # Frequency range
frq = frq[:len(frq)//2]      # Only first half is taken

fourier_x_list = fft(x_list)
abs_fourier_x = [abs(x)/len(fourier_x_list) for x in fourier_x_list]

fourier_y_list = fft(y_list)
abs_fourier_y = [abs(y)/len(fourier_y_list) for y in fourier_y_list]


final_fourier_x = abs_fourier_x[:len(abs_fourier_x)//2]
final_fourier_y = abs_fourier_y[:len(abs_fourier_y)//2]


outX = pd.DataFrame({"Fourier_X": final_fourier_x})
outY = pd.DataFrame({"Fourier_Y": final_fourier_y})

writer = pd.ExcelWriter(output_data_path, engine='xlsxwriter')

outX.to_excel(writer, sheet_name="sheet1")
outY.to_excel(writer, startcol=2, index=False, sheet_name='sheet1')
writer.save()

output_file("Graph/FFT_own_x.html")
plot = figure(title="Vibration X fft",
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 0.1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_x)
show(plot)

output_file("Graph/FFT_own_y.html")
plot = figure(title="Vibration Y fft",
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 0.1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_y)
show(plot)
