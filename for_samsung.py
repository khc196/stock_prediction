import csv, datetime

fname = "Samsung Electronics.csv"
fname2 = "Samsung Electronics_new.csv"
split_date = datetime.datetime.strptime("2018.05.03", "%Y.%m.%d").date()
with open(fname,'r') as f:
    sam_reader=csv.reader(f,dialect="excel")
    for row in sam_reader:
        convert_date = datetime.datetime.strptime(row[0], "%Y.%m.%d").date()
        if convert_date <= split_date:
            for i in range(1, 6):
                row[i] = str(int(int(row[i]) / 50))
        with open(fname2, 'a', newline='') as f2:
            sam_writer=csv.writer(f2, dialect="excel")
            sam_writer.writerow(row)
            print(row)

