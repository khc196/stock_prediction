import csv, datetime
import matplotlib.pyplot as plt

fname = "Samsung Electronics_new.csv"

x = []
y = []

with open(fname,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(datetime.datetime.strptime(row[0], "%Y.%m.%d").date())
        y.append(int(row[1]))

plt.plot(x,y, label='CLOSE')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Samsung Electronics Stock Prices')
plt.legend()
plt.show()


