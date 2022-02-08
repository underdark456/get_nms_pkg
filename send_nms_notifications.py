import threading
import os
import re
import smtplib

def mail(text):
  mailserver = smtplib.SMTP('smtp.office365.com', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.login('ishavrov@comtechtel.com', 'pass')
  # Adding a newline before the body text fixes the missing message body
  mailserver.sendmail(f'ishavrov@comtechtel.com', 'ishavrov@comtechtel.com', 'Subject: {}\n\n{}'.format('New NMS 4 Version', '<font face="Courier New, Courier, monospace">' + text + '</font>'))
  mailserver.quit()

os.chdir('c:/Python') # Moving to the mounted directory
dir_template = '\d+\s\d(.\d+){3}' # tempate for the NMS_4 directory name
f1 = os.listdir()

def glob_re(pattern,strings):
    return filter(re.compile(pattern).match, strings)

def Status():
  global f1
  threading.Timer(1.0, Status).start() #Repeate function every n-seconds
  f2 = os.listdir()
  f3 =  set(f2) - set(f1) # Finding the difference between two lists

  if len(f3) == 0: # if no changes in difference i.e "0" - no new files
    pass
  else:
    f1 = os.listdir()
    try:
      re.match(dir_template, list(f3)[0]).group(0)
    except AttributeError:
      print('Shit file')
    else:
      new_version = 'New NMS Version: ',list(f3)[0]
      mail(os.getcwd() + "/" + list(f3)[0])


Status()

