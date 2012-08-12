import time
from modules import irc_settings

#some variables we will need
chan = irc_settings.chan
nick = irc_settings.nick
password = irc_settings.password
holder = []
buffer = ''

#join chan
def joinChan(s):
	s.sendall("JOIN %s \n" % chan)

#set our nickname
def setNick(s):
	s.sendall("NICK %s \n" % nick)

#send identify command to NickServ
def identify(s):
	s.sendall("IDENTIFY %s \n" % password)

#attempt to ghost the current nickname
def ghost(s):
	s.sendall("/msg NickServ GHOST %s :%s \n" % (nick, password))

#send leaving message, then close socket
#Could be a LOT better
def quit(s, reason):
	sendMessage(s, reason)
	time.sleep(1)
	s.close()

#respond to PING requests
def pong(s):
	s.sendall("PONG :pingis")

#use SSL connection
def wrapSSL(socket, nick, password, server):
	port = 6697
	ircsock = ssl.wrap_socket(socket)
	return ircsock

#parse the input line by line
#TODO: separate by type, sender, hostmask, etc
def readLine(s):
	global holder
	global buffer
	while True:
		if len(holder) > 0: #if we have items in buffer, pop and return
			return holder.pop(0)
		buffer = s.recv(1024) #buffer the input
		holder = buffer.split("\n") #split on newline

#sends a message to broadcast to the entire current channel
def sendMessage(s, message):
	message.strip('\n\r')
	s.sendall('PRIVMSG ' + chan + ' :' + message + '\n')