#!/usr/bin/python
# Filename: ml_stats.py

import mailbox

ml_mailbox = 'oss-events.mbox'   # FIXME 
file = 'report.html'            # FIXME

class Author:   # Represents the author of the post (probably a subscriber of the list)
    def __init__(self, name):
        self.mail = mail
        self.posts = 1
        self.started = 0
        self.name = name
        self.date = date

def get_mail(string):   # Rerurns the content between the signs [<, >] 
    x1 = string.find('<') + 1
    x2 = string.find('>')
    return string[x1:x2]

def get_name(mail):    # Returns the name that appears before the @ [at] symbol
    x1 = mail.find('@')
    return mail[:x1]

def get_date(date):    # Converts the Datetime to a Date format
    x1 = date.find(' ') + 1
    x2 = date.replace(' ', '_', 3).find(' ')
    return date[x1:x2]

def get_month(date):    # Return the month from the Day Month Year format
    x1 = date.find(' ') + 1
    x2 = date.replace(' ', '_', 1).find(' ')
    return date[x1:x2]

def get_year(date):     # Returns the year from the Day Month Year format
    x1 = date.replace(' ', '_', 1).find(' ') + 1
    return date[x1:]

auth_dic= {}    # A dictionary that stores all the objects of the 'Author' instance
mbox = mailbox.mbox(ml_mailbox)
for message in mbox:
    mail = get_mail(message['from'])
    name = get_name(mail)
    date = get_date(message['date'])
    month = get_month(date)
    year = get_year(date)
    if (name not in auth_dic):   # If this is author's first mail an object is created
        contact = Author(name)
        auth_dic[name] = contact
    else:
        for contact in auth_dic:
            if auth_dic[contact].name == name:
                auth_dic[contact].posts += 1
                auth_dic[contact].date = date

try:
    f = open(file, 'w')
    content = "<html><head></head><h1>Mailing List stats</h1><table><tr><td>Name</td><td>Mails Sent</td><td>Last message</td></tr>"
    for contact in auth_dic:
        content += "<tr><td>" + str(auth_dic[contact].name) + "</td><td>" + str(auth_dic[contact].posts) + "</td><td>" + str(auth_dic[contact].date) + "</td></tr>"
    content += "</table>"
    f.write(content)
    f.close()
    print file + " was generated succesfully!"
except:
    print "Something went wrong!"
