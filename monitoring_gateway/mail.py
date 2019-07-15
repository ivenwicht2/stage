import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(message):    
    msg = MIMEMultipart()
    msg['From'] = 'support.gateway@nauticspot.fr'
    msg['To'] = 'j.ladoux@nauticspot.fr'
    msg['Subject'] = 'problème gateway' 
    message = str(message)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.ionos.fr', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('support.gateway@nauticspot.fr', 'N@uticspot19')
    mailserver.sendmail("support.gateway@nauticspot.fr","support.gateway@nauticspot.fr","j.ladoux@nauticspot.fr", msg.as_string())
    mailserver.quit()

