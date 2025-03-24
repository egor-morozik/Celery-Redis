from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Celery('tasks', 
             broker='redis://localhost:6379/0', 
             backend='redis://localhost:6379/0')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'your-email@gmail.com'  
EMAIL_PASSWORD = 'your-app-password'  

@app.task
def send_welcome_email(to_email, username):
    subject = 'Добро пожаловать!'
    body = f'Привет, {username}!\n\nСпасибо за регистрацию на нашем сайте. Мы рады тебя видеть!'
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(EMAIL_FROM, EMAIL_PASSWORD)  
        
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()
        
        print(f"Email успешно отправлен на {to_email}")
        return f"Email sent to {to_email}"
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        raise e