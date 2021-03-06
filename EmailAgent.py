import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_ADDRESS = ""
SENDER_PASS = ''

def send_email(recipient, subj = "email from elliot", body = "error with sending email, sorry about that :("):
    mail_content = body
    #The mail addresses and password
    sender_address = SENDER_ADDRESS
    sender_pass = SENDER_PASS
    receiver_address = recipient
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subj
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
