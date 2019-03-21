import math
import sys


datafile = open(sys.argv[1])
X = []
for line in datafile:
    X.append(line.split())
X = [[int(x) for x in x1] for x1 in X]
labelfile = open(sys.argv[2])

Y = []

for line in labelfile:
    Y.append(line.split())
Y = [[int(y) for y in y1] for y1 in Y]


def all_col_average(x):
    assert len(x) > 0
    columns_avg = []
    for i in range(len(x[0])):
        columns_sum = 0
        for j in range(len(x)):
            columns_sum += x[j][i]
        columns_avg.append(float(columns_sum/len(x)))
    return columns_avg


def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_cols = all_col_average(x)
    avg_labels = all_col_average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    col_correlation = []
    temp_data = [[] for i in range(len(x))]
    for i in range(len(x[0])):
        for j in range(len(x)):
            xdiff = x[j][i] - avg_cols[j]
            ydiff = y[j][0] - avg_labels[0]
            diffprod += xdiff * ydiff
            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff
        col_correlation.append(diffprod / math.sqrt(xdiff2 * ydiff2))
    selectedattributes = []
    for index in range(len(col_correlation)):
            if col_correlation[index] > 0.39:
                selectedattributes.append(index)
    for row in range(len(x)):
        for index in range(len(col_correlation)):
            if col_correlation[index] > 0.39:
                temp_data[row].append(x[row][index])
    final_rows = len(temp_data)
    final_cols = len(selectedattributes)
    trainLabels = {}
    # Read the labels and identify the number of class occurence
    n = {0: 0, 1: 0}
    for line in open(sys.argv[2]):
        a = line.split()
        trainLabels[int(a[1])] = int(a[0])
        n[int(a[0])] += 1
    m0 = []
    m1 = []

    for i in range(0, final_cols):
        m0.append(0.0)
        m1.append(0.0)

    # Calculate the sum of each feature/column
    for i in range(0, final_rows):
        for j in range(0, final_cols):
            if trainLabels.get(i) is not None and trainLabels.get(i) == 0:
                m0[j] += float(temp_data[i][j])
            elif trainLabels.get(i) is not None and trainLabels.get(i) == 1:
                m1[j] += float(temp_data[i][j])
    # Calculates the mean --> divide by n
    for i in range(0, len(m0)):
        m0[i] = float(m0[i]/n.get(0))
    for i in range(0, len(m1)):
        m1[i] = float(m1[i]/n.get(1))
    test_data = open(sys.argv[3])
    testdata = []
    for line in test_data:
        testdata.append(line.split())
    zero_class = 0
    one_class = 0
    for i in range(0, len(testdata)):
        d0 = 0.0
        d1 = 0.0
        for j in range(len(selectedattributes)):
            sel_attr = selectedattributes[j]
            d0 += (m0[j] - float(testdata[i][sel_attr]))**2
            d1 += (m1[j] - float(testdata[i][sel_attr]))**2
        if d0 < d1:
            print("%d 0" % i)
            zero_class += 1
        else:
            print("%d 1" % i)
            one_class += 1
    print("Features used", len(selectedattributes))
    print(zero_class)
    print(one_class)

pearson_def(X, Y)
