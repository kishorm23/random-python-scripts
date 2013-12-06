#script to fetch the lyrics of song currently being
#played on rhythmbox client
import os
import urllib
import urllib2
import time
import sys
import thread
import xml.dom.minidom
run=True
def spinning_cursor():
    cursor='/-\|'
    i = 0
    while run:
        yield cursor[i]
        i = (i + 1) % len(cursor)
def wait():
    try:
	    for c in spinning_cursor():
	        sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(0.001)
		sys.stdout.write('\r')
    except:
        print 
def parseLyrics(data):
	data.find('<Lyric>')
	start = data.find('<Lyric>')
	end = data.find('</Lyric>')
	return data[start+len('<Lyric>'):end]
f = os.popen('rhythmbox-client --print-playing-format %tt')
title = f.read()
f = os.popen('rhythmbox-client --print-playing-format %aa')
artist = f.read()
f = os.popen('rhythmbox-client --print-playing-format %ag')
genre = f.read()
if title=='\n' and artist=='\n':
	print "It seems no song is being played on rhythmbox. Play something to get lyrics."
        exit()
a1 = "********************************"
a2 = "Title: "+ title[0:len(title)-1]
a3 = "Artist: "+ artist[0:len(artist)-1]
a4 = "Genre: "+ genre[0:len(genre)-1]
op = "%s\n%s\n%s\n%s\n%s"%(a1,a2,a3,a4,a1)
print op
headers = { 'User-Agent' : 'Mozilla/5.0' ,'Host': 'api.chartlyrics.com','Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',}
url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric"
url += "?artist="+artist+"&song="+title
thread.start_new_thread(wait,())
fp = urllib.urlopen(url,None,headers)
data = fp.read()
try:
	xml = xml.dom.minidom.parseString(data)
	pretty = xml.toprettyxml()
	#print pretty
	LyricId = xml.getElementsByTagName('LyricId')[0].firstChild.nodeValue
	LyricChecksum = xml.getElementsByTagName('LyricChecksum')[0].firstChild.nodeValue
	#print LyricId,LyricChecksum
	url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric"
	url += "?lyricId="+LyricId+"&lyricCheckSum="+LyricChecksum
	time.sleep(20)
	#print url
	fp = urllib.urlopen(url,None,headers)
	data = fp.read()
	lyric=parseLyrics(data)
	os.system('echo '+'"'+op+'\n'+lyric+'" |less')
	run=False
	inp = str(raw_input("\bSave lyrics(y/n)?"))
	if inp=='y' or inp=='Y':
		inp+=a2[len('Title: ')+1:len(a2)]+".lyric"
		try:
			file_w=open(inp,'a')
			file_w.write(op+'\n'+lyric)
		except:
			print "Could not write",inp
except:
	print "\bLyrics not found"

