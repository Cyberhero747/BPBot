from random import choice
from time import strftime
import os

#write to our log file
def writeToLog(line):
	currTime = str(strftime("%Y-%m-%d %H:%M:%S"))
	chanlog = open('chanlog.txt', 'a+')

	chanlog.write(currTime + ' ' + line + '\n')
	chanlog.close()

def closeLog():
	chanlog.flush() #do this just in case
	chanlog.close()

#search and return the keyword(s)
def searchLog(query):
	chanlog = open('chanlog.txt', 'r')
	quoteBuffer = []

	for line in chanlog:
		if query in line and not '.quote' in line: #quoting quote searches is redundant
			quoteBuffer.append(line.strip('\r\n\t'))
	chanlog.close()

	if len(quoteBuffer) == 1:
		return quoteBuffer[0]
	elif len(quoteBuffer) > 1:
		return '[Quote 1 of ' + str(len(quoteBuffer)) + '] ' + choice(quoteBuffer)
	else:
		return 'No matches found for \'' + query + '\''

#Return the current size of chanlog.txt
def getLogSize():
	size = float(os.path.getsize('chanlog.txt')) / 1024
	return ('%.2f' % round(size, 2)) + 'KB'