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
capman = asss.get_interface(asss.I_CAPMAN)
lm = asss.get_interface(asss.I_LOGMAN)

#freqman = asss.get_interface(asss.I_FREQMAN)
#objs = asss.get_interface(asss.I_OBJECTS) not found..

def dev(targ, msg):

	"""Provides chat function for development. Must be Mod+ to view.
	
	On client-> profile-> auto (underneath chats), or ?devmode in game. 
	
	Targ can be either p or arena."""

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
	""" Command to toggle ?demode """
	if not hasattr(p, 'devmode'): p.devmode = True
	elif p.devmode: p.devmode = False
	else: p.devmode = True
	
# Freq to event map

EventMap = {
	
	0 : 'pub',
	1 : 'pub',
	2 : 'prac',
	3 : 'prac',
	4 : 'bab',
	5 : 'bab',	
	6 : 'soccer',
	7 : 'soccer',
	8 : 'duel',
	9 : 'duel',
	101 : None,
	69: 'spec'};

def get_event(freq):
	""" Returns player event based on freq number.
	defaults to event pub to allow for use of private freqs."""
	return EventMap.setdefault(freq, 'pub')

def innkz(x, y):
	""" Primary safezone coords """
	if x > 7888 and x < 8496:
		if y > 7888 and y < 8480:
			return True
	return False

# Maps freq number to proper event safezone.
# point - [x, y] single point like duel.
# box - [x, x, y, y] random placement in side box.
# radius [x, y, radius] random placement in side circle.
	
map_to_safezone = {
	2 : ['box', 215, 237, 600, 622],
	3 : ['box', 215, 237, 600, 622],
	4 : ['radius', 847, 817, 12],
	5 : ['radius', 847, 817, 12],	
	6 : ['box', 800,820,347,355],
	7 : ['box', 800,820,461,469],
	8 : ['point', 461, 830],
	9 : ['point', 570, 934]};

def getP(name):
	""" Returns pointer to player or None """
	_p = [0]
	def each_player(p):
		if str(p.name.lower()) == str(name.lower()):
			_p[0] = p
			return _p[0]
	asss.for_each_player(each_player)
	if isinstance(_p[0], asss.PlayerType):
		return _p[0]
	return None

def mm_attach(arena):
	arena.lib_devmode = asss.add_command("devmode", devmode, arena)

def mm_detach(arena):
	for attr in ['lib_devmode']:
		try: delattr(arena, attr)
		except: pass
