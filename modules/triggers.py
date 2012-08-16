from __init__ import *

_triggers = []

#cycle through all triggers and, if loaded, deliver the
#appropriate response to the chan
def findTriggers(s, user, nick, hostmask, type, chan, msg):
	if isIgnored(hostmask):
		return #don't check for triggers from ignored users
	else:
		print '<<< MSG IS: ' + str(msg)
		if type == 'INVITE':
			acceptInvite(msg[1:])
			return
		if msg == 'quit' and nick == 'BradPitt':
			quit(s, 'Leaving!')
			return
		if msg == 'IL':
			sendMessage(s, showList(s))
			return
		if re.match('\.iu\s(.*)', str(msg)):
			host = re.match('\.iu\s(.*)', str(msg)).group(1)
			sendMessage(s, ignoreUser(host, nick))
		urlFinder = re.search('(http(s)?://([^/#\s]+)[^#\s]*)(#|\\b)', msg, re.I | re.S)
		if urlFinder != None:
			sendMessage(s, isValidPage(urlFinder.group(1)))

#split the line into logical parts
def parseLine(s, currLine):
	line = currLine.split()
	try:
		if line[1] == 'PRIVMSG':
			user = line[0]
			nick = getNick(user)
			hostmask = getHostmask(user)
			type = line[1]
			chan = line[2]
			msg = ' '.join(line[3:])
			findTriggers(s, user, nick, hostmask, type, chan, msg[1:])
		if line[1] == 'INVITE':
			acceptInvite(s, line[3][1:])
		if len(line) == 2: #most likely a ping, or server alert
			if line[0] == 'PING':
				pong(s)
	except IndexError:
		pass

	# There are still a few other types of messages we will get
	# from the server, but this will be done via trial and error
	# I guess?