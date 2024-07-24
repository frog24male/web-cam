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