#!/usr/bin/env python
import mailbox, sys, re, pyratemp
from os import path
from optparse import OptionParser
from pprint import pprint #FIXME debug only


# Dictionary of Authors
class Authors:
    def __init__(self):
        self.authors = {}

    def parse_msg(self, msg):
        if (msg.from_mail not in self.authors):
            author = Author(msg.from_mail, msg.date)
            self.authors[msg.from_mail] = author
        else:
            self.authors[msg.from_mail].posts += 1
            self.authors[msg.from_mail].lastmsgdate = msg.date

    def parse_log_file(self):
        f = open(mbfile+"/logs/subscribe", "r")
        prog = re.compile("(^[^(]*)[^ ]*[ ]([^:]*)[:][ ]([dn])[^ ]*[ ]([^,;]*).*$") 
        registered = []
        for line in f.readlines():
            r = prog.match(line)
            if r.group(4) in self.authors.keys() and r.group(3) == 'n':
                self.authors[r.group(4)].subscrdate = r.group(1)[:-1] #FIXME store timestamp
                if r.group(4) not in registered:
                    registered.append(r.group(4))
                
        for author in self.authors.keys():
            if author not in registered:
                self.authors.pop(author)


    def print_authors(self):
        for author in self.authors:
            print(self.authors[author])

# Represents the author of the post probably a subscriber of the list
class Author:
    def __init__(self, mail, date):
        self.mail = mail
        self.posts = 1
        self.started = 0
        self.lastmsgdate = date
        self.subscrdate = ""
    def __str__(self):
        return self.mail+" "+str(self.posts)+" "+str(self.started)+" "+self.lastmsgdate+" | "+self.subscrdate

class Message:
    def __init__(self, message):
        self.from_mail = self.get_mail(message['from'])
        self.date = self.get_date(message['date'])
        self.month = self.get_month(self.date)
        self.year = self.get_year(self.date)
        
    # Returns the content between the signs [<, >] 
    def get_mail(self, string):
        x1 = string.find('<') + 1
        x2 = string.find('>')
        return string[x1:x2]

    # Converts the Datetime to a Date format FIXME store timestamp!
    def get_date(self, date):
        x1 = date.find(' ') + 1
        x2 = date.replace(' ', '_', 3).find(' ')
        return date[x1:x2]

    # Return the month from the Day Month Year format
    def get_month(self, date):
        x1 = date.find(' ') + 1
        x2 = date.replace(' ', '_', 1).find(' ')
        return date[x1:x2]

    # Returns the year from the Day Month Year format
    def get_year(self, date):
        x1 = date.replace(' ', '_', 1).find(' ') + 1
        return date[x1:]


if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] <Mailman's root directory>")
    parser.add_option("-g", "--graph", default=False, dest="graph", action="store_true", help="Add graphs to the report")
    parser.add_option("-m", "--minimal", default=False, dest="minimal", action="store_true", help="") #FIXME help text
    parser.add_option("-o", "--output", default="report.html", dest="output", help="Use this option to rename the output file or change the save path. Default: ./report.html")
    (options, args) = parser.parse_args()

    # Arguments validation
    if len(args) < 1:
        parser.print_help()
        sys.exit()
    
    if not path.isdir(args[0]) or not path.exists(args[0]+"/archives") or not path.exists(args[0]+"/logs"):
        print "lala" #FIXME error msg
        sys.exit()

    mbfile = args[0]
    outputfile = options.output
    authors = Authors()

    if options.minimal:
         mbox = mailbox.mbox(mbfile)
    else:
         mbox = mailbox.mbox(mbfile+"/archives/private/team.mbox/team.mbox") # FIXME We should ask which mailing list to select

    # Parse all messages in mbox file
    for message in mbox:
        msg = Message(message)
        authors.parse_msg(msg)    

    # Generate extended info
    if not options.minimal:
        authors.parse_log_file()
    
    #authors.print_authors() #FIXME Debug info
    
    f = open(outputfile, 'w')
    a = authors.authors
    t = pyratemp.Template(filename='report.tpl')
    result = t(mydic=a)
    f.write(result)
    f.close()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
