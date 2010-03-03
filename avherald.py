#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib2 import urlopen
import re
import datetime
import PyRSS2Gen as RSS2
import hashlib

# Get the source of the home page
# Change the 'opt' for filters
req = urlopen('http://avherald.com/h?list=&opt=0')

# Find all links to the articles
relativeArticleLinks = re.findall('/h\?article=[a-f0-9/]*&opt=\d', req.read())

# Build complete link and store in array
articleLinks = []
for relativeArticleLink in relativeArticleLinks:
    articleLinks.append('http://avherald.com' + relativeArticleLink)

# Initialize the rss feed
rss = RSS2.RSS2(
    language = "en-US",
    copyright = "Copyright (c) 2008-2010, by The Aviation Herald",
    title = "Aviation Herald News",
    link = "http://www.avherald.com/",
    description = "Incidents and News in Aviation",
    lastBuildDate = datetime.datetime.utcnow())

# Do the actual work!
for articleLink in articleLinks:
    
    articleRequest = urlopen(articleLink)
    articleRaw = articleRequest.read()
    
    titlereg = re.findall('<span class="headline_article">.*?</span>', articleRaw)
    titler = titlereg[0]     # Title of Article
    titler = titler[31:-7]
    
    datereg = re.findall('<span class="time_avherald">.*?</span>', articleRaw)
    dater = datereg[0]
    dater = dater[28:-7]
    
    dateyr = re.findall('[0-9]{4}', dater)                      # Find raw year
    datemr = re.findall(' [A-Z][a-z]{2} ', dater)               # Find raw month
    datedr = re.findall('[0-9]{1,2}[r,s,t,n,d,h]{2,3}', dater)  # Find raw day
    datetr = re.findall('[0-9]{2}:[0-9]{2}Z', dater)            # Find raw time
    #print dateyr, datemr, datedr, datetr
    
    # Time Published
    datey = dateyr[1]     # Year
    datem = datemr[1]
    datem = datem.strip()
    
    dmonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for x in range(12):
        if datem == dmonth[x]:
            datem = x+1   # Month
            break
    
    dated = datedr[1]
    dated = dated.rstrip('rstndh')    # Day
    
    datet = datetr[1]
    dateth = datet[:-4]   # Hour
    datetm = datet[3:-1]  # Minute
    
    subjectreg = re.findall('<span class="sitetext">.*?</span>', articleRaw)
    subjectr = subjectreg[3]
    # Add the Date in small grey font to the Article
    subjectr = "<font size=-1 color=\"grey\">" + dater + "<br><br\\><br><br\\></font>" + subjectr[23:-7]
    
    # Print the stuff, so it looks cool
    print datey, datem, dated, dateth, datetm
    print titler
    
    # Add Item to the rss feed
    rss.items.append(RSS2.RSSItem(
                title = titler,
                link = articleLink,
                description = subjectr,
                # Sometimes, articles get updated without an url change, thats why a checksum, isPermalink = false
                guid = RSS2.Guid(hashlib.sha1(subjectr).hexdigest(),0),
                pubDate = datetime.datetime(int(datey),int(datem),int(dated),int(dateth),int(datetm))))

pathToFile = "/some/directory/on/local/hdd/or/server/"
rss.write_xml(open(pathToFile + "aviationherald.xml", "w"))
