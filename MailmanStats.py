#!/usr/bin/env python
import mailbox, sys, re, pyratemp, time, pickle
from os import path, walk, mkdir
from optparse import OptionParser
from pychart import *
from pprint import pprint #FIXME debug only

### CLASSES ###
# Dictionary of Authors
class Authors:

    def __init__(self):
        self.authors = {}
        self.sorted_authors_emails = []
        self.sorted_authors_threads = []
        self.totalmails = 0                                                                                                                                                                                
        self.totalthreads = 0
        self.totalmonth = {}
        self.prevmsgtime = 0

    def parse_msg(self, msg):
        if (msg.from_mail not in self.authors):
            author = Author(msg.from_mail, msg.date)
            self.authors[msg.from_mail] = author
            self.totalmails += 1
        else:
            self.totalmails += 1
            self.authors[msg.from_mail].posts += 1
            self.authors[msg.from_mail].lastmsgdate = msg.date
            self.authors[msg.from_mail].lastmsgdatestr= time.ctime(msg.date)
        if "Re:" not in msg.subject:
            self.authors[msg.from_mail].started += 1
            self.totalthreads += 1
        else:
            if msg.date - self.prevmsgtime < self.authors[msg.from_mail].shorttime: self.authors[msg.from_mail].shorttime = msg.date - self.prevmsgtime
            if msg.date - self.prevmsgtime > self.authors[msg.from_mail].longtime: self.authors[msg.from_mail].longtime = msg.date - self.prevmsgtime
        if msg.month not in self.totalmonth: self.totalmonth[msg.month] = 1
        if msg.month not in self.authors[msg.from_mail].monthdic: self.authors[msg.from_mail].monthdic[msg.month] = 1
        else: 
            self.authors[msg.from_mail].monthdic[msg.month] += 1
            self.totalmonth[msg.month] += 1
        self.prevmsgtime = msg.date

    def parse_dates(self):
        for a in self.authors:  
            pass    # Throws ValueError: timestamp out of range for platform time_t Probably needs another converter
            #self.authors[a].shorttime = time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.authors[a].shorttime))
            #self.authors[a].longtime = time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.authors[a].longtime)) 

    def print_authors(self):
        for author in self.authors:
            print(self.authors[author])

    def sort_authors(self):
        self.sorted_authors_emails = sorted(self.authors, key=lambda x:self.authors[x].posts, reverse=True)
        self.sorted_authors_threads = sorted(self.authors, key=lambda x:self.authors[x].started, reverse=True)

    def create_pages(self):
        for a in self.authors:
            f = open(outputdir+"/ml-files/"+self.authors[a].pagename, 'w')
            t = pyratemp.Template(filename='user.tpl')
            result = t(author=self.authors[a])
            f.write(result)

    def plotEmailsPerAuthor(self):
        tmp = []
        for a in self.sorted_authors_emails:  
            tmp.append([a, authors.authors[a].posts])
        plotBarGraph(tmp, outputdir+"/ml-files/ml-emailsperauthor.png", "Authors", "Emails")

    def plotThreadsPerAuthor(self): #FIXME sorting
        tmp = []
        for a in self.sorted_authors_threads:
                tmp.append([a, authors.authors[a].started])
        plotBarGraph(tmp, outputdir+"/ml-files/ml-threadsperauthor.png", "Authors", "Threads")

# Represents the author of the post probably a subscriber of the list
class Author:
    def __init__(self, mail, date):
        self.mail = mail
        self.posts = 1
        self.started = 0
        self.lastmsgdate = date
        self.lastmsgdatestr = time.ctime(date)
        self.firstmsgdate = time.ctime(date) 
        self.name = self.get_name(self.mail)
        self.pagename = self.get_pagename(self.mail)
        self.monthdic = {}
        self.shorttime = 999999999999999999999999999999999999
        self.longtime = 0

    def get_pagename(self, mail):
        mail = mail.replace('@', 'at')
        return  "ml-" + mail + ".html"

    def get_name(self, mail):
        at = mail.find('@')
        return mail[:at]
 
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
            self.month = self.get_month(r.group(1))

    def get_month(self, date):
        x1 = date.find(' ') + 1
        x2 = date.replace(' ', '_', 2).find(' ')
        return date[x1:x2].replace(' ', '_')
        
    # Returns the content between the signs [<, >] 
    def get_mail(self, string):
        x1 = string.find('<') + 1
        x2 = string.find('>')
        return string[x1:x2]

### GLOBAL FUNCTIONS ###
def plotBarGraph(data, outputfile, xlabel, ylabel):
    theme.output_format = "png"
    theme.output_file = outputfile
    theme.scale_factor = 1.5
    theme.use_color = True
    theme.reinitialize()
    xaxis = axis.X(format=lambda x: "/a80/T"+x, label="/b/15"+xlabel, tic_label_offset=(-5,0))
    yaxis = axis.Y(label="/b/15"+ylabel, format="%d")
    fs = fill_style.Plain(bgcolor=color.lightblue)
    ar = area.T(size = (500,400), x_coord = category_coord.T(data, 0), x_axis = xaxis, y_axis = yaxis, y_range = (0,None), legend = None)
    ar.add_plot(bar_plot.T(data = data, fill_style = fs))
    ar.draw()

def get_mlname(mboxpath):
    dot = path.basename(mboxpath).find(".")
    return path.basename(args[0])[:dot]

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] <mbox file>")
    parser.add_option("-g", "--graph", default=False, dest="graph", action="store_true", help="Add graphs to the report")
    parser.add_option("-o", "--output", default="./", dest="output", help="Use this option to change the output directory. Default: Current working directory.")
    (options, args) = parser.parse_args()
    # Arguments validation
    if len(args) < 1:
        parser.print_help()
        sys.exit()

    if not path.isfile(args[0]):
        print "This is not a file!"
        sys.exit()

    mbox = mailbox.mbox(args[0])
    outputfile = "ml-report.html"
    outputdir = options.output
    authors = Authors()
    mlname = get_mlname(args[0])

    # Create Directory for extra files
    try:
        mkdir(outputdir+"/ml-files/")
    except OSError:
        pass


    # Parse all messages in mbox file
    for message in mbox:
        msg = Message(message)
        authors.parse_msg(msg)

    authors.parse_dates() 
    authors.create_pages() 
    authors.sort_authors()

    #authors.print_authors() #FIXME Debug info
    
    f = open(outputfile, 'w')
    t = pyratemp.Template(filename='report.tpl')
    result = t(heading=mlname, totalmails=authors.totalmails, totalthreads=authors.totalthreads, mydic=authors.authors, sa=authors.sorted_authors_emails)
    f.write(result)
    f.close()

    authors.plotEmailsPerAuthor()
    authors.plotThreadsPerAuthor()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
