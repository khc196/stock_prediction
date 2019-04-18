import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def convert_date(date_bytes):
    return mdates.strpdate2num('%Y.%m.%d')(date_bytes.decode('ascii'))

def sma(a, period):
    sma_list = []
    for i in range(len(a)):
        summ=0
        if i <= len(a)-period:
            for j in range(period):
                summ = summ + a[i+j]
        sma_list.append(summ/float(period))
    return sma_list

date, close, diff, open_, high, low, trade = np.loadtxt("Samsung Electronics_new.csv", delimiter=',', usecols=(0,1,2,3,4,5,6), converters={ 0: convert_date}, unpack=True)

sma_numbers = [1, 10, 20, 60, 120, 200]
labels = ["CLOSE", "SMA(10)", "SMA(20)", "SMA(60)", "SMA(120)", "SMA(200)"]

count = 0
for numbers in sma_numbers:
    se_sma = sma(close, numbers)
    newarray = date[len(date)-len(se_sma):]
    plt.plot_date(x=newarray, y=se_sma, fmt='-', linestyle='solid', label=labels[count])
    count = count + 1
plt.legend(loc='upper left')

plt.plot_date(x=date, y=close, fmt='-', linestyle='-', color='black')
plt.xlabel("Date")
plt.ylabel("Stock price")
plt.suptitle('Samsung Electronics Stock Chart')
plt.show()