############################################################
# Functions used in main
############################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime as dt
import os

def read_mailing_list(mailing_list_path):
  # Get Mailing List and Info into a dict
  mailing_list_dict = {}
  with open(mailing_list_path, "r") as mailing_list:
    mailing_list.readline() # header
    for line in mailing_list.readlines():
      line = line.split("\t")
      company_details = {'EMAIL_TO': '' ,'COMPLIMENT': '', 'REQUESTS': '', 'BENEFITS': ''}
      company_details['EMAIL_TO'] = line[2]
      company_details['COMPLIMENT'] = line[3]
      company_details['REQUESTS'] = line[4]
      company_details['BENEFITS'] = line[5]
      mailing_list_dict[line[1]] = company_details
  return mailing_list_dict


def encode_atachment(attachment_path):
  # Encode attachment in MIMEBase, returns object part
  print(f"Encoding attachment {attachment_path} ...")
  attachment = open(attachment_path, 'rb')
  file_name = os.path.basename(attachment_path)
  part = MIMEBase('application','octet-stream') # Creates attachment object
  part.set_payload(attachment.read())
  part.add_header('Content-Disposition',
                  'attachment',
                  filename=file_name)
  encoders.encode_base64(part)
  return part

def build_list(company_dict_key, company_dict):
  items_list = [item.strip() for item in company_dict[company_dict_key].split('|')]
  html_list = ""
  for item in items_list:
    html_list += f"<li>{item}</li>"
  return html_list

def build_message(COMPANY_NAME, company_dict, message_path):
  # Builds customised message based on template message.html and
  # company info from mailing_list_dict[COMPANY_NAME]
  company_dict['REQUESTS'] = build_list('REQUESTS', company_dict)
  company_dict['BENEFITS'] = build_list('BENEFITS', company_dict)
  message_str = open(message_path,"r").read()
  message_str = message_str.format(**company_dict, COMPANY_NAME=COMPANY_NAME)
  return message_str


def encode_message(msg, message_str, EMAIL_FROM, EMAIL_TO, subject):
  msg['From'] = EMAIL_FROM
  msg['To'] = EMAIL_TO # Can also be a string of emails sep by ,
  msg['Subject'] = subject
  msg.attach(MIMEText(message_str, 'html'))
  return msg

def make_new_log_report():
  '''
  Create a new tab-delimited .txt file with headers,
  stored in the current working directory
  returns the name of the log report file
  '''
  date = dt.now().date().strftime('%Y-%m-%d')
  logname = "output/mailbot_log_" + date + ".txt"
  with open(logname, "a+") as logfile:
    logfile.write("Time Started\tTime Completed\tCompany Name\tEmail\tStatus\n")
  print(f"New log report created: {logname}")
  return logname

def append_log_report(logname, sendmail_output):
  '''
  logname: file name of lof report created earlier

  sendmail_output:
  .sendmail on smtp object will return a dictionary, where each
  key-value pair is the recipient to whom the delivery failed.
  '''
  with open(logname, "a+") as logfile:
    logfile.write("\t".join(sendmail_output) + "\n")
