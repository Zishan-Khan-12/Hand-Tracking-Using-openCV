import cv2
import time
import numpy as np
import Handtrackingmodule as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####Parameters######
wCam,hCam = 640, 480
pTime=0
detector = hm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()

minvol=volrange[0]
maxvol=volrange[1]
volbar=400
vol=0
volper=0


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

while True:
    success,img =cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist) !=0:

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),12,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)

        # Hand Range is 50 - 300
        # Volume range is -65 -0
        vol = np.interp(length,[50,250],[minvol,maxvol])
        volbar = np.interp(length,[50,250],[400,150])
        volper = np.interp(length,[50,250],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volper)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1.2,(255,0,0),3)



    cv2.imshow("Img",img)
    cv2.waitKey(1)