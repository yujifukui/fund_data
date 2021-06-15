import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import account

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = account.user
smtp_password = account.password

to_address = "yuji.1399.rk@icloud.com"
from_address = smtp_user
subject = "基準価額表を更新しました"
body = "基準価額表を自動更新しました。内容をご確認ください。"

filepath = "/Users/yuji.f/desktop/fund_data/price_list.xlsx"
filename = os.path.basename(filepath)

msg = MIMEMultipart()
msg["Subject"] = subject
msg["From"] = from_address
msg["To"] = to_address
msg.attach(MIMEText(body, "html"))

with open(filepath, "rb") as f:
    mb = MIMEApplication(f.read())

mb.add_header("Content-Disposition", "attachment", filename=filename)
msg.attach(mb)

s = smtplib.SMTP(smtp_server, smtp_port)
s.starttls()
s.login(smtp_user, smtp_password)
s.sendmail(from_address, to_address, msg.as_string())
s.quit()