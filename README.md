# Hand-Gesture-Mouse-Control
This is an OpenCV application to control all mouse actions based on hand movement. 
This program requires the user to hold 3 objects of a specific color which are nowhere else in the frame. Try finger caps or wrapping colored
paper around fingers. Based on number of objects detected, the mouse events are performed. I suggest wrapping green paper around thumb, index finger and middle finger.
1.Showing all 3 fingers distant enough will move the cursor.
2.If two fingers are brought closely, right click is enabled.
3.Showing 1 finger/ bringing all 3 fingers closely will drag objects.
For simplicity, I used only 3 basic libraries/modules: OpenCV, numpy and pyautogui. No other module/library has been used.
