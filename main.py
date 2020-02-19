'''
NTU ODAC 2019/2020
Bizmag - William
Sends customised email to a mailing list
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime as dt
import os

import functions as fn

############################################################
# Sender Account Details
############################################################

EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_FROM = "odacntu@gmail.com"
FROM_PASSWORD = input("Enter your email password: ")
subject = "NTU ODAC Partnership Proposal 19/20"

# RECIPIENT_NAMES = ["William", "Lyndon"]
# RECIPIENT_LIST = ["lynd0002@e.ntu.edu.sg"] #, "lynd0002@e.ntu.edu.sg"

############################################################
# Main loop
############################################################

# Connect to TLS
smtpObj = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
smtpObj.ehlo() # Expect 250 in the returned tuple, signifying success
smtpObj.starttls() # 220 means server is ready
smtpObj.login(EMAIL_FROM, FROM_PASSWORD) # 235 Authentication successful

# Get mailing list
mailing_list_path = "dependencies/mailing_list.txt"
mailing_list_dict = fn.read_mailing_list(mailing_list_path)

# Encode attachments
attachments = ["dependencies/ntu_odac_partnership_proposal_1920.pdf"]
for attachment in attachments:
  part = fn.encode_atachment(attachment)

message_path = "dependencies/message.html"

# Make new log report
logname = fn.make_new_log_report()

# Iterate through companies
for COMPANY_NAME in mailing_list_dict.keys():
  EMAIL_TO = mailing_list_dict[COMPANY_NAME]['EMAIL_TO']
  # Substitute company info
  message_str = fn.build_message(COMPANY_NAME, mailing_list_dict[COMPANY_NAME], message_path)
  # Create msg object
  msg = MIMEMultipart() # Creates message object
  msg = fn.encode_message(msg, message_str, EMAIL_FROM, EMAIL_TO, subject)
  # Attach pdf encoded earlier
  msg.attach(part)
  # Send email
  time_start = dt.now().strftime("%Y-%m-%d %H:%M:%S")
  print(f"{time_start}: Sending to {EMAIL_TO} ...")
  failures = smtpObj.sendmail(EMAIL_FROM, [EMAIL_TO, "wirriamm@gmail.com"], msg.as_string())

  status = "Not sent"
  if failures == {}:
    status = "Sent"

  time_end = dt.now().strftime("%Y-%m-%d %H:%M:%S")
  print(f"{time_end}: {status} to {EMAIL_TO}.")

  sendmail_output = [time_start, time_end, COMPANY_NAME, EMAIL_TO, status]
  fn.append_log_report(logname, sendmail_output)

  #End of loop

# Disconnect from TLS
smtpObj.quit()
print("Logged out of email.")
