import smtplib
from email.mime.text import MIMEText

    
def email(msg):
    message = MIMEText(msg)
    message['Subject'] = 'gateway error'

    message['From'] = '@source'
    message['To'] = '@dest'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('@source','mdp')
    server.send_message(message)
    server.quit()
