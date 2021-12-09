from tkinter.constants import ACTIVE, CENTER, DISABLED, END
from tkinter.font import NORMAL
from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os
import numpy as np
import pandas as pd
import face_recognition



class Application:
    def __init__(self, output_path="./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0)  # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.textNumber=None
        # self.Label=None
        self.root = tk.Tk()  # initialize root window
        # set window title
        self.root.title("Face attendence Model-capturing images")
        self.root.resizable(0,0) 
        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        F= ("Helvetica",16,"italic")
        self.lb=tk.Label(self.root, text="Start Face Recognition",font=F,justify=CENTER,fg="blue")
        self.lb.pack()
        time_now = datetime.datetime.now()
        self.tStr = time_now.strftime('%H:%M')
        self.dStr = time_now.strftime('%d/%m/%Y')
        self.lb1=tk.Label(self.root, text="Date-"+self.dStr,font=F,justify=CENTER,fg="red")
        self.lb1.pack()
        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.pack(padx=10, pady=10)
        # create a textfield
        
        self.textNumber=tk.Entry(self.root,font=F)
        self.textNumber.pack(fill="both",pady=20) 
        self.textNumber.insert(0, "Enter Your Name")
        self.textNumber.configure(state=DISABLED)
        def on_click(event):
            self.textNumber.configure(state=NORMAL)
            self.textNumber.delete(0, END)

            # make the callback only work once
            self.textNumber.unbind('<Button-1>', on_click_id)

        on_click_id = self.textNumber.bind('<Button-1>', on_click)
        # create a button, that when pressed, will take the current frame and save it to file
        self.btn = tk.Button(self.root, text="Capture",state="disabled",command=self.take_snapshot)
        self.btn.pack(fill="both", expand=True, padx=10, pady=4)
        # button for face recognition
        self.btn1=tk.Button(self.root,text="start face recognition",command=self.video_loop)
        self.btn1.pack(fill="both",expand=True,padx=10,pady=4)
        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        # self.video_loop()
        
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            # convert colors from BGR to RGBA
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            # convert image for tkinter
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    self.lb['text']=name
                    self.btn['state']="disabled"
                    dStr=self.dStr
                    markAttendance(name,dStr)
                else :
                    self.lb['text']="NOT MATCHED"
                    self.btn['state']="normal"     
                    print("not matched")
                    print("here you are new so that's why first you capture your image.")
                    
        # call the same function after 30 milliseconds
        self.root.after(30, self.video_loop)
   
    def take_snapshot(self):
        """ Take snapshot and save it to the file """
        if self.textNumber['text']=="Enter Your Name" :
            print("Enter your name")
        else:    
            filename = f'Training_images/'+self.textNumber.get()+'.png'  # construct filename
            p = os.path.join(self.output_path, filename)  # construct output path
            self.current_image.save(p,'png')  # save image as png file
            print("saved {}".format(filename))
   
    def destructor(self):
        """ Destroy the root object and release all resources """
        df=pd.read_csv("attendence.csv")
        df.drop_duplicates(subset=['Name','Date'], inplace=True)
        df.to_csv('attendence.csv', index=False) 
        print("closing...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
# print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
# print(classNames)
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]    
        encodeList.append(encode)
    return encodeList


def markAttendance(name,dStr):
    with open('attendence.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        timenow=datetime.datetime.now()
        t=timenow.strftime("%I:%M %p %A")
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name  in nameList:
            f.writelines(f'\n{name},{t},{dStr}')
                           
encodeListKnown = findEncodings(images)
print('Encoding Complete')
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
                help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
print("starting...")
pba = Application(args["output"])
pba.root.mainloop()
