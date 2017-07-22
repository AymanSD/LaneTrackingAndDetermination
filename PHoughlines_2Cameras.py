
#########################################################################################################################################
######################################################### Lane Detection and Tracking ###################################################
#########################################################################################################################################


import numpy as np
import cv2
import math
import statistics as st

##Capturing video:

cap = cv2.VideoCapture('pa0007.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
##out = cv2.VideoWriter('lanes.avi',fourcc, 20.0, (1024,576))

while True:
    
    _, frame = cap.read()
       
        
## Area o Interest, Negative 
    AoI1 = frame[100:140,10:355]
    AoI2 = frame[100:140,375:720]
    Gray1 = cv2.cvtColor(AoI1, cv2.COLOR_BGR2GRAY)
    Gray2 = cv2.cvtColor(AoI2, cv2.COLOR_BGR2GRAY)


## Colour Filtering
    
##    Lower = np.array([0])
##    Upper = np.array([255])
##    Mask1 = cv2.inRange(Gray1, Lower, Upper)
##    Mask2 = cv2.inRange(Gray2, Lower, Upper)
##    Result1 = cv2.bitwise_and(AoI1,AoI1, Mask1, Mask1)
##    Result2 = cv2.bitwise_and(AoI2,AoI2, Mask2, Mask2)


## Binary Image
    
    edge1 = cv2.Canny(Gray1, 500, 50, apertureSize = 3)
    edge2 = cv2.Canny(Gray2, 500, 50, apertureSize = 3)

    


## Probablistic Hough Lines Transform

    minLineLength = 10
    maxLineGap = 10
    font = cv2.FONT_HERSHEY_SIMPLEX
    

    lines1 = cv2.HoughLinesP(edge1,1,np.pi/180,10,minLineLength,maxLineGap)
    lines2 = cv2.HoughLinesP(edge2,1,np.pi/180,10,minLineLength,maxLineGap)
    points1 = [[]]
    points2 = [[]]
    X11 = [[]]
    X12 = [[]]
    if np.any(lines1) and np.any(lines2):
        for i in range(0, len(lines1)):
            for j in range(0, len(lines2)):
                for x11,y11,x21,y21 in lines1[i]:
                    for x12,y12,x22,y22 in lines2[j]:
                                              
                        cv2.line(AoI1,(x11,y11),(x21,y21),(0,0,255),5)
                        points1[0].append((x11, y11, x21, y21))
                        X11[0].append((x11))
                        Right1 = max(max(X11))
                        Left1 = min(min(X11))
                        middle1 = int(st.mean([Left1, Right1]))
                        ImageCentre = 170
                        cv2.line(AoI2,(x12,y12),(x22,y22),(0,0,255),5)
                        points2[0].append((x12, y12, x22, y22))
                        X12[0].append((x12))
                        Right2 = max(max(X12))
                        Left2 = min(min(X12))
                        Dis2Centre11 = ImageCentre - Left1
                        Dis2Centre12 = Right1 - ImageCentre
                        Dis2Centre21 = ImageCentre - Left2
                        Dis2Centre22 = Right2 - ImageCentre
                        
                        Lane = [[]]
                        if  (Dis2Centre11) > (Dis2Centre12):
                            if (Dis2Centre21) > (Dis2Centre22):
                                Lane = 'Lane 2'
                                cv2.putText(frame, Lane, (100,250), font, 1, (200, 255,20), 3, cv2.LINE_AA)
                            else:
                                break
                        elif Dis2Centre11 < Dis2Centre12:
                            if Dis2Centre21 < Dis2Centre22:
                                Lane = 'Lane 1'
                                cv2.putText(frame, Lane, (100,220), font, 1, (200, 255,20), 3, cv2.LINE_AA)
##                            elif (Dis2Centre21) < (Dis2Centre22):
##                                Lane = 'Lane 1'
##                                cv2.putText(frame, Lane, (100,220), font, 1, (200, 255,20), 3, cv2.LINE_AA)
                            
                        else:
                            break

                print(Dis2Centre11,Dis2Centre12,Dis2Centre21,Dis2Centre22, Lane)                                             



        cv2.imshow('frame', frame)
##        cv2.imshow('Edge1', edge1)
    else:
        continue
        
    k = cv2.waitKey(1) & 0xFF
    if  k == 27:
         break

cap.release()
##out.release()
cv2.destroyAllWindows()
