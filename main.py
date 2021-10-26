import os
from tkinter import *
import cv2
cam = cv2.VideoCapture(0)
img_counter = 0

if not cam.isOpened():
    raise IOError("Cannot open webcam")
while True:
    ret, frame = cam.read()
        # font=cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(frame,'Press space to Capture Image',(100,100),font,1,(0,0,0),2)
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Capture Your Image", frame)
    k = cv2.waitKey(1)
    if k == ord("q"):
        print("closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        A=input("ENTER YOUR NAME----")
        img_name = f'Training_images/'+A+'.png'.format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} Captured..!".format(img_name))
        img_counter += 1
        
        # root=Tk()
        # root.title ("CAPTURING IMAGES")
        # root.geometry("300x300")
        # root.minsize(450,150)
        # root.maxsize(450,150)  
        # F= ("Helvetica",16,"italic")
        # lb=Label(root, text="ENTER YOUR NAME AND SAVE IMAGE",font=F,justify=CENTER,fg="blue")
        # lb.pack()
        # textNumber=Entry(root,font=F)
        # textNumber.pack(fill=Y,pady=20)
        # b1=Button(root,text='SUBMIT',font=F,justify=CENTER,fg="red")
        # b1.pack() 
cam.release()
cv2.destroyAllWindows()
# root.mainloop()