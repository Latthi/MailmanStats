#!/usr/bin/env python
import mailbox, sys, re, pyratemp, time
from os import path, walk
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
            self.authors[msg.from_mail].lastmsgdatestr= time.ctime(msg.date)

    def parse_log_file(self):
        f = open(rootdir+"/logs/subscribe", "r")
        prog = re.compile("(^[^(]*)[^ ]*[ ]([^:]*)[:][ ]([dn])[^ ]*[ ]([^,;]*).*$") 
        registered = []
        for line in f.readlines():
            r = prog.match(line)
            t = time.strptime(r.group(1)[:-1], '%b %d %H:%M:%S %Y')
            if r.group(4) in self.authors.keys() and r.group(3) == 'n':
                self.authors[r.group(4)].subscrdate =  time.mktime(t)
                self.authors[r.group(4)].subscrdatestr = time.asctime(t)
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
        self.lastmsgdatestr = time.ctime(date)
        self.subscrdate = 0 
        self.subscrdatstr = ""
    def __str__(self):
        return self.mail+" "+str(self.posts)+" "+str(self.started)+" "+self.lastmsgdate+" | "+self.subscrdate

class Message:
    def __init__(self, message):
        self.from_mail = self.get_mail(message['from'])
        r = re.match("[^,]*[,][ ]([A-Za-z0-9: ]*)", message['date'])
        t = time.strptime(r.group(1)[:-1], '%d %b %Y %H:%M:%S')
        self.date = time.mktime(t)
        
    # Returns the content between the signs [<, >] 
    def get_mail(self, string):
        x1 = string.find('<') + 1
        x2 = string.find('>')
        return string[x1:x2]

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
        print "Invalid Mailman's root directory!"
        sys.exit()

    rootdir = args[0]
    outputfile = options.output
    authors = Authors()

    if options.minimal:
         mbox = mailbox.mbox(rootdir)
    else:
        mboxes = {}
        i = 0
        for (path, dirs, files) in walk(rootdir):
            for f in files:
                if 'mbox' in f:
                    i += 1
                    dot = f.find(".")
                    ml = f[:dot]
                    f = path + "/" + f
                    print "[" + str(i) + "] " + ml
                    mboxes[i] = f
        choice = input("Choose your mailing list: ")
        mbpath =  mboxes[choice]
        mbox = mailbox.mbox(mbpath)

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
