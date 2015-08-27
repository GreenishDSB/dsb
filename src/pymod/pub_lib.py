###################################################################
# Module: pub_lib.py 
# Prefix: lib_
# Contributors: Fly,
###################################################################
# Notes: 
#
# Not much going on here yet. 
#
###################################################################

import asss

chat = asss.get_interface(asss.I_CHAT)
game = asss.get_interface(asss.I_GAME)
lm = asss.get_interface(asss.I_LOGMAN)

#-----------------------------------------------------------------
# dev is a simple way to output messages during developments, 
# trace events etc. targ can be either p or arena. You must be 
# logged in as mod+ and have p.devmode set to True. You can use 
# the ?devmode to toggle viewing, or as i do add ?devmode on your 
# client -> profile -> auto (underneath chats).
#-----------------------------------------------------------------

def dev(targ, msg):
	list = asss.PlayerListType()
	if isinstance(targ, asss.PlayerType):
		if getattr(targ, 'devmode', 'False'):
			list.append(targ)
	elif isinstance(targ, asss.ArenaType):
		def listplayer(p):
			if p.arena == targ and \
				getattr(targ, 'devmode', 'False'):
					list.append(p)
		asss.for_each_player(listplayer)
	chat.SendAnyMessage(list, asss.MSG_MODCHAT, 0, None, msg)

def devmode(cmd, params, p, arena):
	if not hasattr(p, 'devmode'): p.devmode = True
	elif p.devmode: p.devmode = False
	else: p.devmode = True

#------------------------------------------------------------------
# Freq to event map
#------------------------------------------------------------------

EventMap = {
	0 : 'pub',
	1 : 'pub',
	2 : 'prac',
	3 : 'prac',
	4 : 'bab',
	5 : 'bab',	
	6 : 'soc',
	7 : 'soc',
	8 : 'duel',
	9 : 'duel',
	69: 'spec'};

def getPEvent(freq):
	return EventMap.setdefault(freq, 'pub')
	
#------------------------------------------------------------------
# Freq safezone map
# point - [x, y] single point like duel 
# box - [x, x, y, y] random placement in side box.
# radius [x, y, radius] random placement in side circle.
#------------------------------------------------------------------

safezone_map = {
	2 : ['box', 215, 237, 600, 622],
	3 : ['box', 215, 237, 600, 622],
	4 : ['radius', 847, 817, 12],
	5 : ['radius', 847, 817, 12],	
	6 : ['box', 800,820,347,355],
	7 : ['box', 800,820,461,469],
	8 : ['point', 461, 830],
	9 : ['point', 570, 934]};

#------------------------------------------------------------------
# Returns pointer to player or None
#------------------------------------------------------------------

def getP(name):
	player = [0]
	def each_player(p):
		if str(p.name.lower()) == str(name.lower()):
			player[0] = p
			return player[0]
	asss.for_each_player(each_player)
	if isinstance(player[0], asss.PlayerType):
		return player[0]
	return None
	
#------------------------------------------------------------------

def mm_attach(arena):
	arena.lib_devmode = asss.add_command("devmode", devmode, arena)

def mm_detach(arena):
	for attr in ['lib_devmode']:
		try: delattr(arena, attr)
		except: pass
