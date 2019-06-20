import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


input_data_path = r"C:\Users\Kathi\Desktop\Vibration Analysis\Vibration Data.xlsx"
output_data_path = r"C:\Users\Kathi\Desktop\Vibration Analysis\Vibration Data Rewritten1.xlsx"
vibration_data = pd.read_excel(input_data_path)

# Separating the values of X and Y axis data
vibraX = pd.DataFrame(vibration_data, columns=['VibraX'])
vibraY = pd.DataFrame(vibration_data, columns=['VibraY'])

# Fourier transforms gives the result in X + Yj form
fourier_x = np.fft.fft(vibraX)
fourier_y = np.fft.fft([np.sin(2*np.pi*i*50) for i in range(500)])

# Only the Real part is extracted
fourier_y = fourier_y.real
fourier_x = fourier_x.real

# The ndarray is converted into a list
fourier_x_list = []
for i in fourier_x:
    fourier_x_list.append(i[0])


fourier_y_list = []
for i in fourier_y:
    fourier_y_list.append(i)

Fs = 1

y = fourier_y_list

n = len(y)                       # length of the signal
k = np.arange(n)
print(k)
T = n/Fs
frq = k/T                        # two sides frequency range

Y = fourier_y/n              # fft computing and normalization
print(Y)
plt.plot(frq, abs(Y))
plt.xlabel('freq (Hz)')
plt.ylabel('Y')

plt.show()
