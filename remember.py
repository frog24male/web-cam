import cv2
import time
import streamlit as st
from datetime import datetime
import glob
import os
import smtplib
import ssl
from email.message import EmailMessage
import imghdr


EMAIL="fa7222518@gmail.com"
Password="crac wuun exsg lmcl"
Receiver="frog24male@gmail.com"
def send_email(image_path):

    email_message=EmailMessage()
    email_message["Subject"]="New object enteredd the frame"
    email_message.set_content("An unknown object was detected you should check it")

    with open(image_path,"rb") as file:
        content=file.read()
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))

    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL,Password)
    gmail.sendmail(EMAIL,Receiver,email_message.as_string())
    gmail.quit()


    print("Done")

# Email function (to be implemented as needed)
# from emailing import send_email

# Function to clean up the images folder
def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

# Initialize Streamlit app
st.title("Motion Detector")
start = st.button('Start Camera')

# If the 'Start Camera' button is pressed
if start:
    streamlit_image = st.image([])
    video = cv2.VideoCapture(0)
    time.sleep(1)

    first_frame = None
    status_list = [0, 0]
    count = 1

    while video.isOpened():
        status = 0
        check, frame = video.read()

        if not check:
            st.error("Failed to read from camera.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        now = datetime.now()

        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) < 5000:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            if rectangle.any():
                status = 1
                cv2.imwrite(f"./images/{count}.png", frame)
                count += 1
                all_images = glob.glob("images/*.png")
                if all_images:
                    index = int(len(all_images) / 2)
                    image_with_object = all_images[index]

        status_list.append(status)
        status_list = status_list[-2:]

        if status_list[0] == 1 and status_list[1] == 0:
            # send_email(image_with_object)
            clean_folder()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        streamlit_image.image(frame)

        # Break loop if 'q' is pressed (useful for debugging outside of Streamlit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
else:
    st.warning("Click the 'Start Camera' button to begin.")
