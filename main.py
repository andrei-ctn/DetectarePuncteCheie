import cv2
from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use("fivethirtyeight")

# variabile
A4 = (297, 210)  # h,w=w,h
x_max = 0
y_max = 0
x_min = 99999
y_min = 99999

# incarcarea imaginii
img = cv2.imread('input_image.png')
img = cv2.resize(img, A4)
h, w, _ = img.shape
tip=''
#conversie in gri
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# calcul minVal si maxVal cu sigma=0.5
sigma = 0.5
medie_pixeli = np.median(gray)
minVal = int(max(0, (1.0-sigma)*medie_pixeli))
maxVal = int(min(255, (1.0+sigma)*medie_pixeli))
# lista in care se stocheaza x,y punctelor
x_y = []
# detectarea marginilor folosind Canny edge detector
edges = cv2.Canny(gray, minVal, maxVal)
"""
cv2.imshow('Canny', edges)
cv2.waitKey()
"""
var = input('Introduceti tipul obiectului:forma(f)/text(t):')

if var == "f":
    forma = input("Introduceti tipul formei(d,p,t,c): ")
    for x in range(0, edges.shape[0]):  # 0,lungime
        for y in range(0, edges.shape[1]):  # 0,latime
            if edges[x, y] == 255:
                if x > x_max and y > y_max:
                    x_max = x
                    y_max = y

                elif x < x_min and y < y_min:
                    x_min = x
                    y_min = y

                elif x > x_max and y < y_min:
                    x_max = x
                    y_min = y

                elif x < x_min and y > y_max:
                    x_min = x
                    y_max = y

    if forma == "d" or forma == "p":
        tip = 0
        x_y_max = [[x_max, y_max]]
        x_y_min = [[x_min, y_min]]
        x_max_y_min = [[x_max, y_min]]
        x_min_y_max = [[x_min, y_max]]
        x_y = x_y + x_y_max + x_y_min + x_max_y_min + x_min_y_max

    elif forma == "t":
        tip = 0
        x_max_y_min = [[x_max, y_min]]
        x_y_min = [[x_min, y_min]]
        x_med = int((x_max+x_min)/2)
        x_med_y_max = [[x_med, y_max]]
        x_y = x_y + x_max_y_min + x_y_min + x_med_y_max
    elif forma == "c":
        x_y_max = [[x_max, y_max]]
        x_y_min = [[x_min, y_min]]
        x_med = int((x_max+x_min)/2)
        y_med = int((y_max+y_min)/2)
        x_y_med = [[x_med, y_med]]
        x_y += x_y_min + x_y_med + x_y_max
        raza=np.sqrt((x_min-x_med)**2+(y_min-y_med)**2)
        tip = int(raza)

    x_y = np.asarray(x_y)
    # print(x_y)
    #print('Numar puncte={}'.format(len(x_y)))
    x, y = np.transpose(x_y)
    data = [x_y.tolist(), tip]
    plt.scatter(x, y)
    plt.show()
    with open('coordonate.txt', 'w') as f:
        #np.savetxt(f, data)
        f.write('%s\n' % data)
        print(10*'-'+'Datele s-au salvat in coordonate.txt'+10*'-')


elif var == "t":
    array = []
    nr = 0
    for x in range(0, edges.shape[0]):  # 0,lungime
        for y in range(0, edges.shape[1]):  # 0,latime
            if edges[x, y] == 255:
                x_y += [[x, y]]
    for i in range(0, len(x_y)-1):
        if x_y[i][0] > 129 and x_y[i][0] < 131:
            array.append(x_y[i])
        elif x_y[i][1] < 87:  # conturul de jos
            if x_y[i][0] == x_y[i+1][0]:
                if np.abs(x_y[i][1]-x_y[i+1][1]) != 2:
                    array.append(x_y[i])
        else:
            if x_y[i][0] == x_y[i+1][0]:
                if np.abs(x_y[i][1]-x_y[i+1][1]) >= 2:
                    array.append(x_y[i+1])
    array = np.asarray(array)
    array = array[array[:, 0].argsort()]  # ordonez pe y
    x_y = []
    for j in range(0, len(array)-1):
        if array[j][0] == array[j+1][0]:
            if np.abs(array[j][1]-array[j+1][1]) <= 1:
                x_y.append(array[j+1])
        else:
            x_y.append(array[j])
    x_y = np.asarray(x_y)
    print(x_y)
    print('Numar puncte={}'.format(len(x_y)))

    x, y = np.transpose(x_y)

    plt.scatter(x, y)
    plt.show()

    with open('coordonate.txt', 'w') as f:
        np.savetxt(f, x_y)
