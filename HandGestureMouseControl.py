"""
1.Green
lowerBound=np.array([35,80,40])
upperBound=np.array([102,255,255])

2. Red
lowerBound=np.array([150,40,80])
upperBound=np.array([190,255,255])

"""

#importing requirements
import cv2
import numpy as np
import pyautogui

#helper function to calculate distance to achieve more accuracy
def distance(p1,p2):
    return((((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2))**0.5)

#function to drag mouse to a specific location
def drag(p):
    pyautogui.mouseDown()
    pyautogui.moveTo(p[0],p[1])
    pos=pyautogui.position()
    while pos!=p:
        pass

#function to move mouse to a specific location
def move(p):
    global rCount
    rCount=0
    pyautogui.moveTo(p[0],p[1])
    pos=pyautogui.position()
    while pos!=p:
        pass   

#initialising dimensions of screen and webcam 
(sx,sy)=pyautogui.size()
(camx,camy)=(320,240)

#declaring range of color to use(I'm using GREEN here) 
lowerBound=np.array([35,80,40])
upperBound=np.array([102,255,255])


cam= cv2.VideoCapture(0)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

#flags to denote change in events
hFlag=0
rCount=0
timeFlag=0

while True:
    #take image from webcam and resize it 
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))

    #converting image to HSV format
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #creating a mask to show only green items in the picture
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    #draw contours around green objects
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #select an event based on number of green objects in the image
    if(len(conts)==3):
        #3 green objects in the image will move the cursor
        try:
            #find dimensions of the green objects
            x,y,w,h=cv2.boundingRect(conts[0])
            x1,y1,w1,h1=cv2.boundingRect(conts[1])
            x2,y2,w2,h2=cv2.boundingRect(conts[2])
            
            #if the previous event is not "MOVE", then set hflag=2
            if(hFlag<2):
                hFlag=2
                pyautogui.mouseUp()
                
            #draw rectangles around detected objects
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
            cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)

            #find center of each rectangle and consider each center as vertex of a triangle
            cx=x+w//2
            cy=y+h//2
            cx1=x1+w1//2
            cy1=y1+h1//2
            cx2=x2+w2//2
            cy2=y2+h2//2
            #find midpints of the lines joining the triangle
            mid1=((cx+cx1)//2,(cy+cy1)//2)
            mid2=((cx1+cx2)//2,(cy1+cy2)//2)
            mid3=((cx2+cx)//2,(cy2+cy)//2)
            #find position of centroid and move cursor based on it.
            #centroid of a triangle=centroid of triangle formed from midpoints of its edges
            centroid=((cx+cx1+cx2)//3,(cy+cy1+cy2)//3)
            #find absolute location of centroid on the screen
            loc=(int(sx-(centroid[0]*sx/camx)),int(centroid[1]*sy/camy))
            #draw line to show edges connecting the green objects
            cv2.line(img, (cx,cy),(cx1,cy1),(255,0,0),2)
            cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
            cv2.line(img, (cx,cy),(cx2,cy2),(255,0,0),2)
            #draw circle around the midpoints of lines formed
            cv2.circle(img,mid1,(w+h)//5,(0,0,255),2)
            cv2.circle(img,mid2,(w1+h1)//5,(0,0,255),2)
            cv2.circle(img,mid3,(w2+h2)//5,(0,0,255),2)
            
            #find length of the 3 lines
            dist=[]
            countd=0
            dist.append(distance((cx,cy),(cx1,cy1)))
            dist.append(distance((cx1,cy1),(cx2,cy2)))
            dist.append(distance((cx,cy),(cx2,cy2)))
            #if more than 1 line is of lesser length than required, then consider it as a single green object and enable drag function
            for i in dist:
                if i<40:
                    countd+=1
            if countd>1:
                drag(loc)
            else:
                move(loc)
        except:
            pass
        
    elif(len(conts)==2):
        #2 green objects in the image will enable right click
        #if the previous event is not "RIGHT CLICK", then set hflag=0
        if(hFlag>0):
            pyautogui.mouseUp()
            hFlag=0
        #find dimensions of the green objects
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        
        timeFlag=1
        #if width of a rectangle is too high(two green objects close enough to consider as one) then clear timeFlag
        #if width of a rectangle is too low(3 green objects are present but one is not visible due to insufficient light) then clear timeFlag    
        if (w1>35 and w1<52):
            timeFlag=0
        elif (w2>35 and w2<52):
            timeFlag=0
        elif(min(w1,w2)<20):
            timeFlag=0
       
        #draw rectangles around detected objects
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        #find center of each rectangle and use them to draw a line
        cx1=x1+w1//2
        cy1=y1+h1//2
        cx2=x2+w2//2
        cy2=y2+h2//2
        #find midpoint of the line joining the points
        mid=((cx1+cx2)//2,(cy1+cy2)//2)
        #find absolute location of midpoint on the screen
        loc=(int(sx-(mid[0]*sx/camx)),int(mid[1]*sy/camy))

        #draw line to show edge connecting the green objects
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        #draw circle around the midpoint of line formed
        cv2.circle(img, (mid[0],mid[1]),2,(0,0,255),2)

        #if distance is too low enable drag(opencv identifying 1 object as multiple because of more exposure)
        #even now if the timeFlag is 1, then enable right click
        dist=distance((cx1,cy1),(cx2,cy2))
        if dist<46:
            drag(loc)
        elif timeFlag==1:
            pyautogui.click(button='right')
            timeFlag=0
            
    elif(len(conts)==1):
        #1 green object in the image will drag the cursor/enables "LEFT CLICK" based on rCount
        try:
            #find dimensions of the green object
            x,y,w,h=cv2.boundingRect(conts[0])
            #set hFlag=1 to denote entering this event
            hFlag=1
            #increment rCount to denote entering this condition consecutively, in 2 successive frames
            rCount+=1
            #if entered this condition for considerable amount of time, clear timeFlag
            if rCount>10:
                timeFlag=0 
            elif rCount>0 and rCount<4:
                timeFlag=1

            #draw rectangle around detected object
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #find center of the rectangle and drag cursor based on its position on screen
            cx=x+w//2
            cy=y+h//2
            cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
            loc=(int(sx-(cx*sx/camx)),int(cy*sy/camy))
            
            #if timeFlag is 1, press "left click" else enable drag
            if timeFlag==1:
                pyautogui.click()
            else:
                drag(loc)
                
        except Exception as e:
            print(e)
    cv2.imshow("cam",img)
    #close application on pressing "esc"
    key=cv2.waitKey(1)
    if key==27:
        break
cam.release()
cv2.destroyAllWindows()

    
