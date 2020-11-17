import argparse

import cv2
import pandas as pd

csv = pd.read_csv(f'../resources/colors.csv')

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
arguments = vars(ap.parse_args())

img = cv2.imread(arguments['image'])

clicked = False
r = g = b = 0


def getColorName(red, green, blue, cname=None):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(red - int(csv.loc[i, "R"])) + abs(green - int(csv.loc[i, "G"])) + abs(blue - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


def draw_function(click_event, x, y, *args):
    if click_event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, clicked
        clicked = True

        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        color_name = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        cv2.putText(img, color_name, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if r + g + b >= 600:
            cv2.putText(img, color_name, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
