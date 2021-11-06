from tkinter.constants import CENTER
from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os
import numpy as np
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
        self.lb=tk.Label(self.root, text="ENTER YOUR NAME AND SAVE IMAGE",font=F,justify=CENTER,fg="blue")
        self.lb.pack()
        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.pack(padx=10, pady=10)
        # create a textfield
        
        self.textNumber=tk.Entry(self.root,font=F)
        self.textNumber.pack(fill="both",pady=20) 
       
        # create a button, that when pressed, will take the current frame and save it to file
        btn = tk.Button(self.root, text="Capture",
                        command=self.take_snapshot)
        btn.pack(fill="both", expand=True, padx=10, pady=4)
        # button for face recognition
        btn1=tk.Button(self.root,text="Attendence")
        btn1.pack(fill="both",expand=True,padx=10,pady=4)

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        self.video_loop()
        
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
                    # y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    # cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
                else :
                    print("not matched")
                    print("here you are new so that's why first you capture your image.")
                    
        # call the same function after 30 milliseconds
        self.root.after(30, self.video_loop)
   
    def take_snapshot(self):
        """ Take snapshot and save it to the file """
      #   ts = datetime.datetime.now() # grab the current timestamp
       
        filename = f'Training_images/'+self.textNumber.get()+'.png'  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        self.current_image.save(p,'png')  # save image as jpeg file
        print("saved {}".format(filename))

    # def face(self):
    #     print("start face recognition")
    #     while True:
    #         ok, frame = self.vs.read()  # read frame from video stream
    #         if ok:  # frame captured without any errors
    #             # convert colors from BGR to RGBA
    #             cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    #             self.current_image = Image.fromarray(
    #                 cv2image)  # convert image for PIL
    #             # convert image for tkinter
    #             imgtk = ImageTk.PhotoImage(image=self.current_image)
    #             self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
    #             self.panel.config(image=imgtk)  # show the image
    #         imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    #         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #         facesCurFrame = face_recognition.face_locations(imgS)
    #         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    #         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
    #             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    #             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    #             # print(faceDis)
    #             matchIndex = np.argmin(faceDis)

    #             if matches[matchIndex]:
    #                 name = classNames[matchIndex].upper()
    #                 print(name)
    #                 y1, x2, y2, x1 = faceLoc
    #                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
    #                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #                 cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    #                 cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    #                 markAttendance(name)
    #      # call the same function after 30 milliseconds
    #         self.root.after(30, self.face)    
    def destructor(self):
        """ Destroy the root object and release all resources """
        print("closing...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('attendence.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tStr},{dStr}')

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