#!/usr/bin/env python3

import PIL
import pyshark
import matplotlib.pyplot as plot

position_X = 0
position_Y = 0
buttonNotHoldCounter = 0
X = []
Y = []
drawing_index = 0
isNewDrawing = True

capture = pyshark.FileCapture('sniffed.pcapng', display_filter="btatt")

def save_drawing(x_coords, y_coords, index):
    figure = plot.figure()
    ax1 = figure.add_subplot()
    ax1.scatter(x_coords, y_coords, s=1)
    ax1.set_xlim(-500, 0)
    ax1.set_ylim(100, 700)
    figure.savefig(f'drawing_{index}.png')
    plot.close(figure)

for packet in capture:
    data = packet['btatt'].value.split(":")
    press = int(data[0], 16)
    delta_x = int(data[1], 16)
    delta_y = int(data[3], 16)

    if delta_x > 127:
        delta_x -= 256
    if delta_y > 127:
        delta_y -= 256

    position_X += delta_x
    position_Y += delta_y

    if press:
        if buttonNotHoldCounter >= 10 and not isNewDrawing:
            if len(X) >= 50:
                save_drawing(X, Y, drawing_index)
                drawing_index += 1
            X = []
            Y = []
        isNewDrawing = False
        X.append(position_X)
        Y.append(-position_Y)
        buttonNotHoldCounter = 0
    else:
        buttonNotHoldCounter += 1

if len(X) >= 50:
    save_drawing(X, Y, drawing_index)
