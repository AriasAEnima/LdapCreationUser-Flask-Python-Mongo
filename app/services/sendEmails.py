import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import config

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "testingaenima@gmail.com"
recipients = ["julianeduardoarias@gmail.com"]


def getServer():
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, config.PASSWORD_ADMIN_TEST_EMAIL)
    return server
    

def sendEmail(server,user, passwordNotEncript):
    email = user['email']
    username = user['username']
    message = MIMEMultipart("alternative")
    message["Subject"] = f"User Credentials {username}"
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    text = f"email : {email}, username: {username}, password: {passwordNotEncript}"
    part1 = MIMEText(text, "plain")
    message.attach(part1) 
    server.sendmail(sender_email, recipients, message.as_string())
