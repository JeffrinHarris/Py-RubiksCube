import cv2, time
import numpy as np
import kociemba
import sys

# Function to find color based on HSV values
def findColor(clr):
    if (170 < clr[0] < 180 or 0 <= clr[0] <= 4)and 100 < clr[1] < 255 and 0 < clr[2] < 255:
        return 'red'
    elif 5 <= clr[0] <= 13 and 100 < clr[1] < 255 and 0 < clr[2] < 255:
        return 'orange'
    elif 14 <= clr[0] <= 23 and 100 < clr[1] < 255 and 0 < clr[2] < 255:
        return 'yellow'
    elif 24 <= clr[0] <= 35 and 100 < clr[1] < 255 and 0 < clr[2] < 255:
        return 'green'
    elif 110 <= clr[0] <= 130 and 50 < clr[1] < 155 and 0 < clr[2] < 255:
        return 'blue'
    else:
        return 'white'

#-U--
#LFRB
#-D--

#-O--
#GWBY
#-R--

##INPUT ORDER URFDLB

# Function to convert color word to Kociemba notation
def findKColor(color):
    if color == 'red':
        return 'D'
    elif color == 'orange':
        return 'U'
    elif color == 'yellow':
        return 'B'
    elif color == 'green':
        return 'L'
    elif color == 'blue':
        return 'R'
    else:
        return 'F'

# Function to convert BGR to HSV
def bgr2hsv(h):
    return cv2.cvtColor(np.uint8([[[h[0], h[1], h[2]]]]), cv2.COLOR_BGR2HSV)[0][0]

cubeSide=''
cubeFull=''

video = cv2.VideoCapture(0)

lowerThreshold = 12
upperThreshold = 28

# minArea = 4700
# maxArea = 8300
minArea = 3700
maxArea = 9300

while True:
    check, frame = video.read()

    minX = 10000
    maxX = 0
    minY = 10000
    maxY = 0

    cubeSide=''

    # # Convert to HSV
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    org = frame

    image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # image = cv2.GaussianBlur(image, (5, 5), 50, 50)

    image = cv2.Canny(image, lowerThreshold, upperThreshold)

    SE = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    image = cv2.dilate(image, SE, iterations=3)

    # # Floodfill from point (0, 0)
    # h, w = image.shape[:2]
    # mask = np.zeros((h+2, w+2), np.uint8)
    # cv2.floodFill(image, mask, (0,0), 255)

    # mask = np.zeros(image.shape[:2], dtype=image.dtype)

    # # blob filter
    # cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # for c in cnts:
    #     area = cv2.contourArea(c)
    #     if area >1000:
    #         # cv2.drawContours(image, [c], -1, 0, -1)
    #         # x,y,w,h = cv2.boundingRect(c)
    #         # cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
    #         cv2.drawContours(mask, [c], 0, (255), -1)


    # Invert mask
    # image = cv2.bitwise_and(image,image,mask= mask)
    image = cv2.bitwise_not(image)

    mask = np.zeros(frame.shape, np.uint8)

    # area filter
    # colors = []
    count = 0
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minArea and area < maxArea:
            # cv2.drawContours(frame, [c], -1, (0,255,0), 3)
            
            x,y,w,h = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
            count += 1

            if x<minX:
                minX = x
            if x+w>maxX:
                maxX = x + w
            if y<minY:
                minY = y
            if y+h>maxY:
                maxY = y + h

            hull = cv2.convexHull(c)
            cv2.drawContours(frame, [hull], -1, (0,count*20,0), 3)

            # mean = cv2.mean(frame[y:y+h,x:x+w])

            # colors.append(str(np.array(mean).astype(np.uint8)))

    # # cv2.drawContours(frame,cnts,-1,(0,255,0),3)
    # cv2.putText(frame, str(colors), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 0, 2)

    # print count in image
    cv2.putText(frame, str(len(cnts)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 0, 2)


    cv2.rectangle(frame, (minX, minY), (maxX, maxY), (36,255,12), 2)   

    for i in range(3):
        for j in range(3):
            MINX=int(minX+(maxX-minX)*j/3)
            MINY=int(minY+(maxY-minY)*i/3)
            MAXX=int(minX+(maxX-minX)*(j+1)/3)
            MAXY=int(minY+(maxY-minY)*(i+1)/3)
            BALX=int((MAXX-MINX)/3)
            BALY=int((MAXY-MINY)/3)
            cv2.rectangle(frame, (MINX+BALX, MINY+BALY), (MAXX-BALX, MAXY-BALY), (0,0,255), 2)
            mean = cv2.mean(org[MINY+BALY:MAXY-BALY,MINX+BALX:MAXX-BALX])
            if i == 0 and j == 0:
                cv2.putText(frame, str(bgr2hsv(mean)), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), 0, 2)
            cv2.putText(frame, findColor(bgr2hsv(mean)), (int(MINX+10), int(MINY+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), 0, 2)
            cubeSide = cubeSide + findKColor(findColor(bgr2hsv(mean)))


    cv2.putText(frame, str(cubeSide), (30,70), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,0,0), 0, 2)
    # hsv=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("Edge", image)
    cv2.imshow("Original", frame)
    # cv2.imshow("Hsv", hsv)
    # cv2.imshow('cutted contour',hsv[MINY:MAXY,MINX:MAXX])
    
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        break

    if key == 32:
        cubeFull = cubeFull + cubeSide

    if key == ord('r'):
        cubeFull = ''

    if key == ord('s'):
        try:
            a = kociemba.solve(cubeFull)
            print(a)
        except Exception as e:
            print(e)
        break

    # if key == ord('w'):
    #     lowerThreshold += 1
    #     print("Lower threshold: " + str(lowerThreshold))

    # if key == ord('s'):
    #     lowerThreshold -= 1
    #     print("Lower threshold: " + str(lowerThreshold))

    # if key == ord('e'):
    #     upperThreshold += 1
    #     print("Upper threshold: " + str(upperThreshold))

    # if key == ord('d'):
    #     upperThreshold -= 1
    #     print("Upper threshold: " + str(upperThreshold))
  
video.release()
  
# Destroying all the windows
cv2.destroyAllWindows()