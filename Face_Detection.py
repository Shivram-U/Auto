#                               Face Detection
import os
import numpy
import cv2
from sre_constants import ANY

from tkinter import*
from tkinter import filedialog

import mysql.connector

from pyttsx3 import*
import speech_recognition as spr

import time
CWD=os.getcwd()
print("$$$$$ Face_Detection Program running in Directory << %s >>$$$$$"%CWD)

global img_count,Data,sql,sql_run,msql
img_count=0
Data={}

class SQL_D:
    def __init__(self):
        global img_count,Data,sql
        sql=mysql.connector.connect( host ="localhost",
                                     user ="root",
                                     passwd="$hivRam@9900#",
                                     database="new")
        server_info=sql.get_server_info()
        print("Connected to the MySQL Server Version:",server_info)
        sql_run=sql.cursor()
        self.run=sql_run
        #sql_run.execute("use new;")
        try:
            sql_run.execute("create table image_analysis (SNO int,Name varchar(255),File_Dir varchar(255),Faces varchar(255));",multi=True)
        except:
            print("Table Already Created.")
        #sql_run.execute("DROP TABLE Image_Analysis;")
        #print(type(sql_run),type(server_info),type(sql))
    def store(self,number,name,dir,faces):
        global img_count,Data,sql,sql_run
        comm=["insert into image_analysis (SNO,Name,File_Dir,Faces) values(%s,'%s','%s','%s');"%(number,name,dir,faces),]
        for i in comm:
            self.run.execute(i,multi=True)
            sql.commit()
    def insert(self,col):
        global img_count,Data,sql,sql_run
        comm=["insert into image_analysis (Faces) values('%s');"%(col)]
        for i in comm:
            self.run.execute(i,multi=True)
            sql.commit()
            

def Access_File(self):
            inp=filedialog.askopenfile(initialdir="/") #return a file directive,if used to acces bring the main content of the file.
            for i in str(inp).split():
                if(i[0:4]=='name'):
                    s=i[5::]
                    break
            return s
def conc(l):
    global img_count
    s=''
    for i in l:
        s+=str(i)
    return s
#print(conc([3,4,3,'d','f2','r23','c','d','2edd','wds','dasda']))
class Face_Detection():
    def __init__(self):
        global img_count,Data,sql,sql_run,msql
        self.Classifier={
                            "face":cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml'),
                            "eye":cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml'),
                            "smile":cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml'),
                            "fullbody":cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_fullbody.xml')
                        }

    class Video:
        def __init__(self):
            global img_count,Data,sql,sql_run,msql,F_D
        def detect_Face(self):
            global img_count,Data,sql,sql_run,msql,F_D
            self.Web_Cam_B=cv2.VideoCapture(0)
            while self.Web_Cam_B.isOpened():
                    ret, frame= self.Web_Cam_B.read()
                    frame=cv2.flip(frame,1)  #mirror the image
                    #print(frame.shape)
                    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    faces=F_D.Classifier["face"].detectMultiScale(gray,6,6)  #detect the face
                    for x,y,w,h in faces:
                        #sending coordinates to Arduino
                        #string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
                        #print(string)
                        #ArduinoSerial.write(string.encode('utf-8'))
                        #plot the center of the face
                        cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
                        #eye :cv2.circle(frame,(x+w//2,y+h//2),50,(0,255,0),2)
                        
                        #plot the roi
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
                        #cv2.circle(frame,(x+w//2,y+h//2),100,(0,255,0),2)
                    #plot the squared region in the center of the screen
                    cv2.rectangle(frame,(640//2-30,480//2-30),
                                 (640//2+30,480//2+30),
                                  (255,255,255),3)
                    #out.write(frame)
                    cv2.imshow('img',frame)
                    #cv2.imwrite('output_img.jpg',frame)
                    '''for testing purpose
                    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
                    time.sleep(0.05)
                    print('data from arduino:'+read)
                    '''
                    # press q to Quit
                    if cv2.waitKey(10)&0xFF== ord('q'):
                        break;
            self.Web_Cam_B.release()
            cv2.destroyAllWindows()
                

    class Image:
            def __init__(self):
                global img_count,Data,sql,sql_run,msql
                img_count+=1
                File=filedialog.askopenfile(initialdir="/") #return a file directive,if used to acces bring the main content of the file.
                print("$",File)
                #print(File.name) #since the the value returned by the filedialog is a class, 
                                #hence the member object name is accessed using dot(.) operator
                File_Path=''
                File_name=''
                for i in File.name:
                    if(i=='/'):
                        File_Path+="\\"
                        File_Path+="\\"
                        File_name=''
                    else:
                        File_Path+=i
                        File_name+=i
                print("%%",File_name)
                self.Orig_Img=cv2.imread(File_Path)

                self.Gr_Img=cv2.cvtColor(self.Orig_Img,cv2.COLOR_BGR2GRAY)
                Data[conc(["img",img_count])]= {    "Name":File_name,
                                                    "Dir":File.name,
                                        "Orig_Img":cv2.imread(File_Path),
                                        "Gr_Img": cv2.cvtColor(self.Orig_Img,cv2.COLOR_BGR2GRAY),
                                        "faces":[],
                                        "eyes":[],
                                        "smile":[]
                                        }

                self.ImgConfig= {"type":"img",
                                "design" :  {
                                            "Shape":["rectangle","circle","putText","line"],
                                            "color":{"red":(0,0,255),"Blue":(255,0,0),"green":(0,255,0)}
                                            }
                                }
                #print(Data)
                #print(len(Data["img1"]["Orig_Img"]))
            def min(a,b):
                    if(a<b):
                        return a
                    else:
                        return b 
            def max(a,b):
                    if(a>b):
                        return a
                    else:
                        return b
            def Detect_Objects(self,count,object):
                    objects=self.Det[object].detectMultiScale(Data[conc(["img",img_count])]["Gr_Img"],scaleFactor=1.1,minNeighbors=6,minSize=(200,20),flags=cv2.CASCADE_SCALE_IMAGE)
                    return objects

            def Faces(self):
                    global img_count,Data,sql,sql_run,msql
                    Data[conc(["img",img_count])]["faces"]=self.Detect_Objects(img_count,"face")
                    #print("|S",Data)
                    #msql.insert(Data[conc(["img",img_count])]["faces"])
                    msql.store(img_count,Data[conc(["img",img_count])]["Name"],Data[conc(["img",img_count])]["Dir"],Data[conc(["img",img_count])]["faces"])
                    for (x,y,w,h) in Data[conc(["img",img_count])]["faces"]:
                                #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
                                cv2.line(self.Orig_Img,(x,y-(h//3)),(x+w,y-(h//3)),(255,0,0),2)
                                print(h,w)
                                cv2.putText(self.Orig_Img,"Shiva",(x,y-(h//3)-1),1,5,(0,255,0),2,cv2.LINE_AA)
                                cv2.circle(self.Orig_Img,(x+w//2,y+h//2),min(h,w),(0,255,0),4)
                                cv2.rectangle(self.Orig_Img,(x,y),(x+w,y+h),(255,0,255),2)
                    self.Orig_Img=cv2.resize(self.Orig_Img,(1350,850),interpolation=cv2.INTER_CUBIC)
                    cv2.imshow("Image_Analysis",self.Orig_Img)
                    cv2.waitKey(100000)

            def Show(self):
                cv2.imshow("Image_Analysis",self.Orig_Img)
                cv2.waitKey(100000)
    
data={"Shiv":"C:\\Users\\udaya\\OnleDrive\\Pictures\\Saved_Pictures\\Shiv.jpeg","family":"C:\\Users\\udaya\\OneDrive\\Pictures\\Camera_Roll\\fam.jpg"}
msql=SQL_D()
#msql.store("meow")
def auto():
    global F_D,Image,Video
    F_D=Face_Detection()
    #Image=F_D.Image()
    Video=F_D.Video()
    Video.detect_Face()
    #Image.Faces()
#msql.run.execute("DROP TABLE Image_Analysis;")
print("||Terminated||")
auto()
    
'''
def detect_object(classifier,data):
    objects=classifier.detectMultiScale(data,scaleFactor=1.1,minNeighbors=6,minSize=(200,20))
    return objects

def show(faces,img):
    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.line(img,(x,y-(h//3)),(x+w,y-(h//3)),(255,0,0),2)
        print(h,w)
        #cv2.circle(img,(x+w//2,y+h//2),min(h,w),(0,255,0),4)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
    cv2.imshow("Here",img)
    cv2.waitKey(100000)
face_d=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

img=cv2.imread(data["Shiv"])
img1=cv2.imread(data["family"])
#grayscale conversion of the given data, for efficient Data analsis
gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
faces=detect_object(face_d,gray)
show(faces,img1)'''

