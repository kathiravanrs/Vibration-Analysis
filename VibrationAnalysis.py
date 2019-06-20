import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d


input_data_path = "Data/Vibration Data - Modified.xlsx"
output_data_path = "Data/Fourier transformed Vibration Data.xlsx"
vibration_data = pd.read_excel(input_data_path)

# Separating the values of X and Y axis data
vibraX = pd.DataFrame(vibration_data, columns=['VibraX'])
vibraY = pd.DataFrame(vibration_data, columns=['VibraY'])

Fs = 1                  # Sampling Frequency of the signal
n = len(vibraY)         # Number of samples
k = np.arange(n)
T = n/Fs
frq = k/T


# Fourier transforms gives the result in X + Yj form
fourier_x = np.fft.fft(vibraX)/n
fourier_y = np.fft.fft(vibraY)/n

# Only the absolute part is needed
fourier_y = abs(fourier_y)
fourier_x = abs(fourier_x)

# The ndarray is converted into a list
fourier_x_list = []
for i in fourier_x:
    fourier_x_list.append(i[0])


fourier_y_list = []
for i in fourier_y:
    fourier_y_list.append(i[0])


outX = pd.DataFrame({"Fourier_X": fourier_x_list})
outY = pd.DataFrame({"Fourier_Y": fourier_y_list})

writer = pd.ExcelWriter(output_data_path, engine='xlsxwriter')

outX.to_excel(writer, sheet_name="sheet1")
outY.to_excel(writer, startcol=2, index=False, sheet_name='sheet1')
writer.save()

# fig, (ax1, ax2) = plt.subplots(1, 2, sharey='col')
# ax1.plot(fourier_x)
# ax2.plot(fourier_y)
#  plt.show()


output_file("plot_x.html")
plot = figure(title="Vibration X fft", plot_width=1500, y_range=Range1d(-0.005, 0.01), plot_height=700)
plot.line(frq, fourier_x_list)
show(plot)

output_file("plot_y.html")
plot = figure(title="Vibration Y fft", plot_width=1500, y_range=Range1d(-0.00001, 0.005), plot_height=700)
plot.line(frq, fourier_y_list)
show(plot)
