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
articleLinks = re.findall('/h\?article=[a-f0-9/]*&opt=\d', req.read())

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
    articleLink = 'http://www.avherald.com' + articleLink
    articleRaw = urlopen(articleLink).read()
    titler = re.findall('<span class="headline_article">.*?</span>', articleRaw)[0][31:-7]    # Title of Article
    dater = re.findall('<span class="time_avherald">.*?</span>', articleRaw)[0][28:-7]
    
    # Time Published
    datey = re.findall('[0-9]{4}', dater)[1]                            # Year
    datem = re.findall(' [A-Z][a-z]{2} ', dater)[1].strip()             # Find Month
    dmonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for x in range(12):
        if datem == dmonth[x]:
            datem = x+1   # Month
            break
    dated = re.findall('[0-9]{1,2}[r,s,t,n,d,h]{2,3}', dater)[1].rstrip('rstndh')  # Day
    datet = re.findall('[0-9]{2}:[0-9]{2}Z', dater)[1]                  # Find Time
    dateth = datet[:-4]   # Hour
    datetm = datet[3:-1]  # Minute
    
    # Add the Date in small grey font to the Article
    subjectr = "<font size=-1 color=\"grey\">" + dater + "<br><br\\><br><br\\></font>" + re.findall('<span class="sitetext">.*?</span>', articleRaw)[3][23:-7]
    
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
