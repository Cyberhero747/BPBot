from __init__ import *
from random import choice
import trigger_booleans

_triggers = []

#cycle through all triggers and, if loaded, deliver the
#appropriate response to the chan
def findTriggers(s, user, nick, hostmask, type, chan, msg):
	msgList = msg.split() #this will help with finding triggers
	if isIgnored(hostmask):
		return #don't check for triggers from ignored users
	else:
		# print '<<< MSG IS: ' + str(msg)
		if type == 'INVITE':
			acceptInvite(msg[1:])

		if msgList[0] == '.trigger' and isAdmin(nick):
			sendMessage(s, toggleTrigger(msgList[1]))

		if msgList[0] == '.quote' and trigger_booleans.quote:
			sendMessage(s, searchLog(' '.join(msgList[1:])))

		if config.nick in msg and trigger_booleans.response:
			sendMessage(s, nameCall())

		units = ['kg', 'lb']
		for x in msgList:
			if any(weight in x for weight in units) and trigger_booleans.conversion:
				sendMessage(s, convert(x))

		zumbaResponse = ['THE BEST WAY TO TONE UP', 'WELCOME TO THE TONEZONE BABY', 'FEEL IT IN YOUR HIPS, GIRL', 'BURNING UP THOSE CALORIES!',
						'NOW WITH 100% MORE HIPS', 'DANCE YOUR SHAME AWAY', 'CARDIO\'S FINEST HOUR']
		if 'zumba' in msg and trigger_booleans.zumba:
			sendMessage(s, choice(zumbaResponse))

		rudeMessages = ['fuck you', 'fuck off', 'fat ', 'loser', 'shut up']
		rudeResponse = ['rude ^', 'rude!', 'rude~', '100% rude']
		if any(x in msg for x in rudeMessages) and trigger_booleans.rude:
			sendMessage(s, choice(rudeResponse))

		# if msgList[0] == '.getmax':
		# 	sendMessage(s, return1RM(msgList[1], msgList[2]))

		# if msgList[0] == '.rm':
		# 	sendMessage(s, insert1RM(nick, msgList[1], msgList[2]))

		if msg == 'quit' and isAdmin(nick):
			quit(s, 'Leaving!')

		if msgList[0] == '.w' and trigger_booleans.weather:
			sendMessage(s, currWeather(' '.join(msgList[1:])))

		if msgList[0] == '.update' and isAdmin(nick):
			reloadSelf(s)

		if msgList[0] == 'IL':
			sendMessage(s, showList(s))

		if msgList[0] == '.logsize':
			sendMessage(s, getLogSize())

		if msgList[0] == '.iu' and isAdmin(nick):
			sendMessage(s, ignoreUser(' '.join(msgList[1:])))

		urlFinder = re.search('(http(s)?://([^/#\s]+)[^#\s]*)(#|\\b)', msg, re.I | re.S)
		if urlFinder != None and trigger_booleans.links:
			sendMessage(s, isValidPage(urlFinder.group(1)))

		if msgList[0] == '.d' and trigger_booleans.decision:
			sendMessage(s, decide(str(msg)))

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
			if logging:
				writeToLog(nick + ' said: ' + msg[1:])
		if line[1] == 'INVITE':
			acceptInvite(s, line[3][1:])
		if len(line) == 2: #most likely a ping, or server alert
			if line[0] == 'PING':
				pong(s)
	except IndexError:
		pass