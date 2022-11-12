import cv2, time
import numpy as np

from imutils import contours

def rgb2hsv(r, g, b):
    return cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]

colors = {
    # 'gray': ([76, 0, 41], [179, 255, 70]),        # Gray
    # 'blue': ([69, 120, 100], [179, 255, 255]),    # Blue
    # 'yellow': ([21, 110, 117], [45, 255, 255]),   # Yellow
    'orange': ([125, 75, 35], [255, 125, 85])     # Orange
    }
  
# Assigning our static_back to None
static_back = None
  
# Capturing video
video = cv2.VideoCapture(0)
# Infinite while loop to treat stack of image as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()

    original = frame.copy()

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Color threshold to find the squares
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    for color, (lower, upper) in colors.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        color_mask = cv2.inRange(image, lower, upper)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, close_kernel, iterations=5)

        color_mask = cv2.merge([color_mask, color_mask, color_mask])
        mask = cv2.bitwise_or(mask, color_mask)

    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # Sort all contours from top-to-bottom or bottom-to-top
    # (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

    # Take each row of 3 and sort from left-to-right or right-to-left
    # cube_rows = []
    # row = []
    # for (i, c) in enumerate(cnts, 1):
    #     row.append(c)
    #     if i % 3 == 0:  
    #         (cnts, _) = contours.sort_contours(row, method="left-to-right")
    #         cube_rows.append(cnts)
    #         row = []

    cv2.imshow('mask', color_mask)

  
    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)
  
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        break
  
video.release()
  
# Destroying all the windows
cv2.destroyAllWindows()

#note the values nigger take all vals then trial error