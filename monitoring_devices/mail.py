import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(message):    
    msg = MIMEMultipart()
    msg['From'] = 't.oriol@nauticspot.fr'
    msg['To'] = 'theo.toriol.lol@gmail.com'
    msg['Subject'] = 'pb device' 
    message = str(message)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.ionos.fr', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('t.oriol@nauticspot.fr', 'N@uticspot19')
    mailserver.sendmail("t.oriol@nauticspot.fr","theo.toriol.lol@gmail.com", msg.as_string())
    mailserver.quit()
