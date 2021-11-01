from tkinter import *
import tkinter.messagebox 
import cv2
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise IOError("Cannot open webcam")
while True:
    ret, frame = cam.read()
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
        def save():
            A=textNumber.get()
            img_counter=0
            img_name = f'Training_images/'+A+'.png'.format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} Captured..!".format(img_name))
            img_counter += 1
            root.withdraw()
            tkinter.messagebox.showinfo("SAVING","Saved Your Image As  "+A+".png")
            root.destroy()
        root=Tk()
        root.title ("SAVING IMAGES")
        root.geometry('450x150+450+50')
        root.resizable(0,0)     
        F= ("Helvetica",16,"italic")
        lb=Label(root, text="ENTER YOUR NAME AND SAVE IMAGE",font=F,justify=CENTER,fg="blue")
        lb.pack()
        textNumber=Entry(root,font=F)
        textNumber.pack(fill=Y,pady=20)    
        b1=Button(root,text='SAVE',font=F,justify=CENTER,fg="red",command=save)
        b1.pack()
        root.mainloop()  
         
cam.release()
cv2.destroyAllWindows()

