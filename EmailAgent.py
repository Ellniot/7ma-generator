import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json

# if email is blocker - go to this URL and enable less secure app access
# https://myaccount.google.com/lesssecureapps   

def send_email(recipient, subj, body):
    SENDER_ADDRESS = ""
    SENDER_PASS = ""
    # load the email and pw from json file
    cred_file_path = "./email_creds.json"
    cred_file_exists = os.path.isfile(cred_file_path)
    if cred_file_exists:
        with open("./email_creds.json") as cred_file:
            parsed_creds = (json.load(cred_file))
            try:
                SENDER_ADDRESS = parsed_creds['email']
                SENDER_PASS = parsed_creds['password']
            except:
                print("Creds file does not contain address or password.")
    else: 
        # TODO create blank email cred file - maybe prompt the user for the email and pw to write to the new file
        # return w/ error
        print("No email credentials file")
        return 0

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
