#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        self.years = []

    def parseMsg(self, msg):
        if (msg.from_mail not in self.authors):
            author = Author(msg.from_mail, msg.date)
            self.authors[msg.from_mail] = author
            self.totalmails += 1
        else:
            self.totalmails += 1
            self.authors[msg.from_mail].posts += 1
            self.authors[msg.from_mail].lastmsgdate = msg.date
            self.authors[msg.from_mail].lastmsgdatestr= time.ctime(msg.date)

        try:
            if "Re:" not in msg.subject or not msg.subject:
                self.authors[msg.from_mail].started += 1
                self.totalthreads += 1
            else:
                if msg.date - self.prevmsgtime < self.authors[msg.from_mail].shorttime: self.authors[msg.from_mail].shorttime = msg.date - self.prevmsgtime
                if msg.date - self.prevmsgtime > self.authors[msg.from_mail].longtime: self.authors[msg.from_mail].longtime = msg.date - self.prevmsgtime
        except TypeError:
            pass

        if msg.month not in self.totalmonth: self.totalmonth[msg.month] = 1
        if msg.month not in self.authors[msg.from_mail].monthdic: self.authors[msg.from_mail].monthdic[msg.month] = 1
        else: 
            self.authors[msg.from_mail].monthdic[msg.month] += 1
            self.totalmonth[msg.month] += 1
        self.prevmsgtime = msg.date

    def calcStats(self):
        self.sortAuthors()
        self.createUserPages()
        self.plotEmailsPerAuthor()
        self.plotThreadsPerAuthor()
        self.plotMonthlyUsage()

    def parseDates(self):
        for a in self.authors:  
            pass    # Throws ValueError: timestamp out of range for platform time_t Probably needs another converter
        #self.authors[a].shorttime = time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.authors[a].shorttime))
            #self.authors[a].longtime = time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.authors[a].longtime)) 

    def sortAuthors(self):
        self.sorted_authors_emails = sorted(self.authors, key=lambda x:self.authors[x].posts, reverse=True)
        self.sorted_authors_threads = sorted(self.authors, key=lambda x:self.authors[x].started, reverse=True)

    def createUserPages(self):
        for a in self.authors:
            f = open(outputdir+"/ml-files/"+self.authors[a].pagename, 'w')
            t = pyratemp.Template(filename='user.tpl')
            result = t(author=self.authors[a], encoding="utf-8")
            f.write(result)

    def plotEmailsPerAuthor(self):
        tmp = []
        for a in self.sorted_authors_emails:  
            tmp.append([a, self.authors[a].posts])
        plotBarGraph(tmp, outputdir+"/ml-files/ml-emailsperauthor.png", "Authors", "Emails")

    def plotThreadsPerAuthor(self):
        tmp = []
        for a in self.sorted_authors_threads:
            tmp.append([a, self.authors[a].started])
        plotBarGraph(tmp, outputdir+"/ml-files/ml-threadsperauthor.png", "Authors", "Threads")

    def plotMonthlyUsage(self):
        months = ["January", "February", "March", "April", "May", "June", "Julu", "August", "September", "Octomber", "November", "December"]
        firstyear = int(min(self.totalmonth.keys())[:4])
        lastyear = int(max(self.totalmonth.keys())[:4])
        firstmonth = int(min(self.totalmonth.keys())[-2:])
        peryear = []
        r = ""
        y = firstyear
        m = firstmonth
        while r != max(self.totalmonth.keys()):
            m += 1
            if m % 12 == 1:
                m = 1
                y += 1
            r = "%i%02d" % (y,m)
            if r not in self.totalmonth:
                self.totalmonth[r] = 0

        for year in range(firstyear, lastyear+1):
            self.years.append(year)
            for yearmonth in self.totalmonth.keys():
                if int(yearmonth[:4]) == year:
                    peryear.append([months[int(yearmonth[-2:])-1], self.totalmonth[yearmonth]])
            peryear = sorted(peryear, key=lambda x: months.index(x[0]))
            plotBarGraph(peryear, outputdir+"/ml-files/ml-usage-"+str(year)+".png", "Months", "Emails")
            peryear = []


    def __str__(self):
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
        self.firstmsgdate = time.ctime(date) 
        self.name = self.getName(self.mail)
        self.pagename = self.getPagename(self.mail)
        self.monthdic = {}
        self.shorttime = sys.maxint
        self.longtime = 0

    def getPagename(self, mail):
        mail = mail.replace('@', 'at')
        return  "ml-" + mail + ".html"

    def getName(self, mail):
        at = mail.find('@')
        return mail[:at]

    def __str__(self):
        return self.mail+" "+str(self.posts)+" "+str(self.started)+" "+str(self.lastmsgdate)

class Message:
    def __init__(self, message):
        self.subject = message['subject']
        prog = re.compile("[A-Za-z0-9._%+-]+[@][A-Za-z0-9.-]+[.][A-Za-z]{2,4}")
        r = prog.search(message['from'])
        if not r:
            raise TypeError
        self.from_mail = r.group(0)
        r = re.match("[^0-9]*([0-9]+[ ]+[A-Za-z]{3}[ ]+[0-9]{4}[ ]+[0-9:]{8}).*", message['date'])
        if r:
            t = time.strptime(r.group(1), '%d %b %Y %H:%M:%S')
            self.date = time.mktime(t)
            self.month = self.getMonth(r.group(1))

    def getMonth(self, date):
        r = re.match("[0-9]+[ ]([A-Za-z]{3})[ ]([0-9]{4}).*", date)
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        month = dictSub(r.group(1), months)
        return "%s%02d" % (r.group(2), int(month))

    # Returns the content between the signs [<, >] 
    def getMail(self, string):
        x1 = string.find('<') + 1
        x2 = string.find('>')
        return string[x1:x2]

### GLOBAL FUNCTIONS ###
def plotBarGraph(data, outputfile, xlabel, ylabel):
    cropped = []
    theme.output_format = "png"
    theme.output_file = outputfile
    theme.scale_factor = 1.5
    theme.use_color = True
    theme.reinitialize()
    for d in data:
        if len(d[0]) > 21:
            cropped.append([d[0][:21]+"...", d[1]])
        else:
            cropped.append([d[0], d[1]])
    xaxis = axis.X(format=lambda x: "/a80/H"+x, label="/b/15"+xlabel, tic_label_offset=(-3,0))
    yaxis = axis.Y(label="/b/15"+ylabel, format="%d")
    fs = fill_style.Plain(bgcolor=color.lightblue)
    ar = area.T(size = (12*len(data)+50,400), x_coord = category_coord.T(cropped, 0), x_axis = xaxis, y_axis = yaxis, y_range = (0,None), legend = None)
    ar.add_plot(bar_plot.T(data = cropped, fill_style = fs, data_label_format="%d", data_label_offset=(2,5)))
    ar.draw()

def getMlName(mboxpath):
    dot = path.basename(mboxpath).find(".")
    return path.basename(args[0])[:dot]


def dictSub(text, dictionary):
    prog = re.compile('|'.join(map(re.escape, dictionary)))
    return prog.sub(str(dictionary[prog.match(text).group(0)]), text)


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
    mlname = getMlName(args[0])

    # Create Directory for extra files
    try:
        mkdir(outputdir+"/ml-files/")
    except OSError:
        pass

    # Parse all messages in mbox file
    for message in mbox:
        try:
            msg = Message(message)
            authors.parseMsg(msg)
        except TypeError:
            continue
        

    authors.calcStats()

    #  Generate ml-report.html
    f = open(outputfile, 'w')
    t = pyratemp.Template(filename='report.tpl')
    result = t(heading=mlname, totalmails=authors.totalmails, totalthreads=authors.totalthreads, mydic=authors.authors, sa=authors.sorted_authors_emails, yr=authors.years)
    f.write(result)
    f.close()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
