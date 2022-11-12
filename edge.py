import cv2, time
import numpy as np

video = cv2.VideoCapture(0)

lowerThreshold = 12
upperThreshold = 28

minArea = 4700
maxArea = 8300

while True:
    check, frame = video.read()

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

    # area filter
    count = 0
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minArea and area < maxArea:
            # cv2.drawContours(frame, [c], -1, (0,255,0), 3)
            
            # x,y,w,h = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
            count += 1

            hull = cv2.convexHull(c)
            cv2.drawContours(frame, [hull], -1, (0,255,0), 3)

            # epsilon = 0.05*cv2.arcLength(c,True)
            # approx = cv2.approxPolyDP(c, epsilon, True)
            # cv2.drawContours(frame, [approx], -1, (0,255,0), 3)
    # print(count)
    # cv2.drawContours(frame,cnts,-1,(0,255,0),3)

    # print count in image
    cv2.putText(frame, str(count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 0, 2)





    cv2.imshow("Edge", image)
    cv2.imshow("Original", frame)
    
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        break

    if key == ord('w'):
        lowerThreshold += 1
        print("Lower threshold: " + str(lowerThreshold))

    if key == ord('s'):
        lowerThreshold -= 1
        print("Lower threshold: " + str(lowerThreshold))

    if key == ord('e'):
        upperThreshold += 1
        print("Upper threshold: " + str(upperThreshold))

    if key == ord('d'):
        upperThreshold -= 1
        print("Upper threshold: " + str(upperThreshold))
  
video.release()
  
# Destroying all the windows
cv2.destroyAllWindows()