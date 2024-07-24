import cv2
import time
from emailing import send_email
import streamlit as st
from datetime import datetime
import glob
import os
from threading import Thread


video=cv2.VideoCapture(0)
time.sleep(1)

first_frame=None
status_List=[]
count=1
def clean_folder():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:

    status=0
    check, frame=video.read()
    gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau=cv2.GaussianBlur(gray_frame, (21,21),0)

    now=datetime.now()

    if first_frame is None:
        first_frame=gray_frame_gau

    delta_frame=cv2.absdiff(first_frame,gray_frame_gau)
    cv2.imshow("Video", delta_frame)
    
    thresh_frame=cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]
    #if line below causes error use kernel=none
    dil_frame=cv2.dilate(thresh_frame,None,iterations=2)
    cv2.imshow("Video", dil_frame)
    countours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in countours:
        if cv2.contourArea(cnt) < 5000:

            continue

        x,y,w,h=cv2.boundingRect(cnt)
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

        if rectangle.any():
            status=1
            cv2.imwrite(f"./images{count}.jpg",frame)
            count=count+1
            all_images=glob.glob("images/*.png")
            index=int(len(all_images)/2)
            image_with_object=all_images[index]
            
    
    status_List.append(status)
    status_List=status_list[-2:]

    if status_List[0]==1 and status_List[1]==0:
        email_thread=Thread(target=send_email,args=(image_with_object, ))
        email_thread.daemon=True

        clean_thread=Thread(target=clean_folder)
        clean_thread.daemon=True
        
        email_thread.start()
        clean_thread.start()
    cv2.imshow("Video", frame)
        
    key=cv2.waitKey(1)

    if key==ord('q'):
        break

video.release()
clean_thread.start()