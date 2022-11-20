import numpy as np
import cv2

# def rgb2hsv(r, g, b):
#     return cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]

# print(rgb2hsv(125, 80, 40))

def hsv2rgb(h, s, v):
    return cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2RGB)[0][0]

print(hsv2rgb(107, 153, 159))

# import kociemba

# try:
#     a = kociemba.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')
#     print(a)
# except Exception as e:
#     print(e)