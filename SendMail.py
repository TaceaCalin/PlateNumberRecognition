# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart
# import socks
# def SendMail(ImgFileName):
#
#     # socks.setdefaultproxy(TYPE, ADDR, PORT)
#     socks.setdefaultproxy(socks.HTTP, 'proxy.proxy.com', 8080)
#     socks.wrapmodule(smtplib)
#
#     smtpserver = 'smtp.live.com'
#     AUTHREQUIRED = 1
#     img_data = open(ImgFileName, 'rb').read()
#     msg = MIMEMultipart()
#     msg['Subject'] = 'subject'
#     msg['From'] = 'tacea.calin96@gmail.com'
#     msg['To'] = 'tacea.calin96@gmail.com'
#
#     text = MIMEText("test")
#     msg.attach(text)
#     image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
#     msg.attach(image)
#
#     s = smtplib.SMTP(smtpserver, 587)
#     s.ehlo()
#     s.starttls()
#     s.ehlo()
#     s.login('tacea.calin96@gmail.com', 'babolat96')
#     s.sendmail('tacea.calin96@gmail.com', 'tacea.calin96@gmail.com', msg.as_string())
#     s.quit()
#
# SendMail("MH67KOP.png")


import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def SendMail(recever):

    gmail_user = 'tacea.calin96@gmail.com'
    gmail_password = 'babolat96'

    sent_from = gmail_user
    # to = 'tacea.calin96@gmail.com'
    img_data = open('MH67KOP.png', 'rb').read()
    image = MIMEImage(img_data, name='MH67KOP')
    text = MIMEText("YEAEAEYSH")
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = 'tacea.calin96@gmail.com'
    msg['To'] = recever
    msg.attach(text)
    msg.attach(image)

    # email_text = """\
    # From: %s
    # To: %s
    # Subject: %s
    #
    # %s
    # """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recever, msg.as_string())
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

SendMail('taceacalin@icloud.com')