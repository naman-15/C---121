import cv2
import time 
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*"XVID")
outputFile = cv2.VideoWriter("output.avi" , fourcc , 20.0 , (720 , 720))

cam = cv2.VideoCapture(0)
time.sleep(2)

bg = 0 

for i in range(60):
    ret , bg = cam.read()

bg = np.flip( bg , axis = 1 )

while(cam.isOpened()):
    ret , img = cam.read()
    if not ret:
        break
    img = np.flip( img , axis = 1 )
    toHSV = cv2.cvtColor( img , cv2.COLOR_BGR2HSV)
    lowerLimit = np.array([30,30,0])
    upperLimit = np.array([104 , 153 , 70])
    mask = cv2.inRange(toHSV , lowerLimit , upperLimit)

    mask = cv2.morphologyEx(mask , cv2.MORPH_OPEN , np.ones( (3 ,3) , np.uint8 ))
    finalMask2 = cv2.bitwise_not(mask)
    resoulution1 = cv2.bitwise_and(img , img , mask = finalMask2 )
    resoulution2 = cv2.bitwise_and( bg , bg , mask = mask)
    finalOutput = cv2.addWeighted( resoulution1 , 1 , resoulution2 , 1 , 0 )
    outputFile.write(finalOutput)
    cv2.imshow("TEST",finalOutput)

    if cv2.waitKey (1) & 0xFF == ord('q'):
        break