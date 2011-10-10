#!/usr/bin/env python
import mailbox, sys, re, pyratemp, time
from os import path, walk
from optparse import OptionParser
from pprint import pprint #FIXME debug only


# Dictionary of Authors
class Authors:
    def __init__(self):
        self.authors = {}
        self.sorted_authors = []

    def parse_msg(self, msg):
        if (msg.from_mail not in self.authors):
            author = Author(msg.from_mail, msg.date)
            self.authors[msg.from_mail] = author
        else:
            self.authors[msg.from_mail].posts += 1
            self.authors[msg.from_mail].lastmsgdate = msg.date
            self.authors[msg.from_mail].lastmsgdatestr= time.ctime(msg.date)
	if "Re:" not in msg.subject: self.authors[msg.from_mail].started += 1

    def print_authors(self):
        for author in self.authors:
            print(self.authors[author])

    def sort_authors(self):
        self.sorted_authors = sorted(self.authors, key=lambda x:self.authors[x].posts, reverse=True)

# Represents the author of the post probably a subscriber of the list
class Author:
    def __init__(self, mail, date):
        self.mail = mail
        self.posts = 1
        self.started = 0
        self.lastmsgdate = date
        self.lastmsgdatestr = time.ctime(date)
    def __str__(self):
        return self.mail+" "+str(self.posts)+" "+str(self.started)+" "+self.lastmsgdate

class Message:
    def __init__(self, message):
        self.subject = message['subject']
        self.from_mail = self.get_mail(message['from'])
        r = re.match("[^,]*[,][ ]+([0-9]+[ ]+[A-Za-z]{3}[ ]+[0-9]{4}[ ]+[0-9:]{8}).*", message['date'])
        if r:
            t = time.strptime(r.group(1), '%d %b %Y %H:%M:%S')
            self.date = time.mktime(t)
        
    # Returns the content between the signs [<, >] 
    def get_mail(self, string):
        x1 = string.find('<') + 1
        x2 = string.find('>')
        return string[x1:x2]

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] <mbox file>")
    parser.add_option("-g", "--graph", default=False, dest="graph", action="store_true", help="Add graphs to the report")
    parser.add_option("-o", "--output", default="report.html", dest="output", help="Use this option to rename the output file or change the save path. Default: ./report.html")
    (options, args) = parser.parse_args()

    # Arguments validation
    if len(args) < 1:
        parser.print_help()
        sys.exit()

    if not path.isfile(args[0]):
        print "This is not a file!"
        sys.exit()

    mbox = mailbox.mbox(args[0])
    outputfile = options.output
    authors = Authors()

    # Parse all messages in mbox file
    for message in mbox:
        msg = Message(message)
        authors.parse_msg(msg)    
    
    authors.sort_authors()

    #authors.print_authors() #FIXME Debug info
    
    f = open(outputfile, 'w')
    a = authors.authors
    b = authors.sorted_authors
    t = pyratemp.Template(filename='report.tpl')
    result = t(mydic=a, sa=b)
    f.write(result)
    f.close()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
