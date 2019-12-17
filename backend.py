import smtplib
def mail(From, to, body):
    gmail_usr = "ENTER EMAIL ADDRESS HERE"
    gmail_password = "ENTER PASSWORD HERE"
  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_usr, gmail_password)
    server.sendmail(From, to ,body)
    server.close()
    print("EMAIL SENT!!!!")

