import pandas as pd
from cmath import pi, exp
from math import log2, ceil
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d


def nxt_power_2(x):
    # Returns the nearest power of 2 larger than given number
    return 2**ceil(log2(x))


def zero_padding(array):
    # Adds a series of 0s to the end of signal such that signal length becomes a power of 2
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
    # Returns the Fourier transformed data as the output


def peak_pos(y_axis, x_axis):
    # Identifies the peaks from the data and returns the position of the peak(Freq) and also the Amplitude of the peak
    peaks = []
    length = len(y_axis)
    mean = sum(y_axis)/length
    # stdev = sqrt(sum(pow(x-mean, 2)/length for x in y_axis))
    for j in range(1, len(y_axis)-1):
        if y_axis[j] > mean and y_axis[j-1] < y_axis[j] > y_axis[j+1]:
            x_value = round(x_axis[j], 2)
            y_value = round(y_axis[j], 2)
            if y_value != 0:
                peaks.append((x_value, y_value))
    return peaks
    # Returns a list of tuples containing an ordered pair of amplitude and frequency


input_data_path = "Data/Vibration Data - Modified.xlsx"
output_data_path = "Data/Fourier transformed Vibration Data.xlsx"
vibration_data = pd.read_excel(input_data_path)

# Separating the values of X and Y axis data
vibraX = pd.DataFrame(vibration_data, columns=['VibraX'])
vibraY = pd.DataFrame(vibration_data, columns=['VibraY'])

# Converting dataframes in to a python list
vibraY = vibraY.values.tolist()
vibraX = vibraX.values.tolist()

# To limit the number or samples
length_fixed = 1024

# To calculate the sum of the data and then average
sum_x, sum_y = 0, 0
for i in range(length_fixed):
    sum_y += vibraY[i][0]
    sum_x += vibraX[i][0]

mean_x = sum_x / length_fixed
mean_y = sum_y / length_fixed

# Mean is subtracted from the data to remove the DC offset (Peak appearing at 0Hz, though there is no DC component)
x_list, y_list = [], []
for i in range(length_fixed):
    x_list.append(vibraX[i][0] - mean_x)
    y_list.append(vibraY[i][0] - mean_y)

# Zeroes are added to the end of the signal
zero_padding(x_list)
zero_padding(y_list)


Fs = 1                          # Sampling Frequency of the signal
n = len(x_list)                 # Number of samples
k = [i for i in range(n)]       # List of values from 0 to n [0, 1, 2, .... 4093, 4094, 4095]
T = n / Fs                      # Total time = No of sample/Sample frequency
frq = [x / T for x in k]        # Frequency range up to Fs/2 (from 0 Hz to 0.5 Hz)
frq = frq[:len(frq) // 2]       # Only first half is taken, because FFT output will be symmetrical


# FFT is applied on the X-Axis data, and then normalised
fourier_x_list = fft(x_list)
abs_fourier_x = [abs(x) / len(fourier_x_list) for x in fourier_x_list]
power_fourier_x = [(abs(x) / len(fourier_x_list))**2 for x in fourier_x_list]


# FFT is applied on the Y-Axis data, and then normalised
fourier_y_list = fft(y_list)
abs_fourier_y = [abs(y) / len(fourier_y_list) for y in fourier_y_list]
power_fourier_y = [(abs(y) / len(fourier_y_list))**2 for y in fourier_y_list]


# Only the left is taken as the output of FT will be symmetrical
final_fourier_x = abs_fourier_x[:len(abs_fourier_x) // 2]
final_fourier_y = abs_fourier_y[:len(abs_fourier_y) // 2]

final_fourier_pwr_x = power_fourier_x[:len(power_fourier_x) // 2]
final_fourier_pwr_y = power_fourier_y[:len(power_fourier_y) // 2]


# FT data is converted to data frame and then exported to a excelsheet
outX = pd.DataFrame({"Fourier_X": final_fourier_x})
outY = pd.DataFrame({"Fourier_Y": final_fourier_y})
outPowerX = pd.DataFrame({"FourierPower_X": final_fourier_pwr_x})
outPowerY = pd.DataFrame({"FourierPower_Y": final_fourier_pwr_y})

writer = pd.ExcelWriter(output_data_path, engine='xlsxwriter')


outX.to_excel(writer, sheet_name="sheet1")
outY.to_excel(writer, startcol=2, index=False, sheet_name='sheet1')
outPowerX.to_excel(writer, startcol=3, index=False, sheet_name='sheet1')
outPowerY.to_excel(writer, startcol=4, index=False, sheet_name='sheet1')

writer.save()

output_file("Graph/FFT_x.html")
plot = figure(title="Vibration X fft - {} samples".format(length_fixed),
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_x)
show(plot)


output_file("Graph/FFT_y.html")
plot = figure(title="Vibration Y fft - {} samples".format(length_fixed),
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_y)
show(plot)

output_file("Graph/Power_x.html")
plot = figure(title="Vibration X fft Power - {} samples".format(length_fixed),
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_pwr_x)
show(plot)


output_file("Graph/Power_y.html")
plot = figure(title="Vibration Y fft Power - {} samples".format(length_fixed),
              x_axis_label='Frequency (Hz)',
              y_axis_label='Amplitude (g)',
              y_range=Range1d(-0.005, 1),
              plot_width=1500,
              plot_height=700)

plot.line(frq, final_fourier_pwr_y)
show(plot)


print("Peaks in Y axis \n (Amp, Frq)\n", peak_pos(final_fourier_pwr_y, frq))
print("Peaks in X axis \n (Amp, Frq)\n", peak_pos(final_fourier_pwr_x, frq))
