###################################################################
# Module: pub_stats.py                                     By: Fly
# Prefix: stats_
###################################################################
# Notes: 
# 
# Everything below #--- needs attention.
# 
# 
###################################################################

from pub_lib import *

class events:
	def __init__(self, event, eventname, eventfreqs, gameId):
		self.event = event
		self.eventname = eventname
		self.eventfreqs = eventfreqs
		self.gameId = gameId
		self.gamestate = 'idle'
		self.captains = []
		self.players = []
		
	def pregame(self):
		self.gamestate = 'pregame'
		
	def start(self):
		self.gamestate = 'running'
		self.gameId += 1
		
	def kill(self):
		self.gamestate = 'idle'
		
		
class stats:
	def __init__(self, name, freq, event, gameId):
		self.name = name
		self.freq = freq
		self.event = event
		self.gameId = gameId
		self.timestamp = 0
		self.kills = 0
		self.deaths = 0
		self.tks = [0,0]
		self.flagtouches = 0
		self.bellflags = 0
		self.balltouches = 0
		self.balltime = 0
		self.ballgoals = 0
		self.killpoints = 0
		self.flagpoints = 0
		self.ballpoints = 0

	def setkills(self, amount = 0):
		self.kills += 1
		self.killpoints += amount	
	def setdeaths(self, amount = 0):
		self.death += 1
		if amount > self.killpoints:
			 amount = self.killpoints
		self.killpoints -= amount
	def settks(self, case, amount=0):
		self.tks[case] += 1
		if case == 0:
			self.killpoints -= amount

	def setflagpoints(self, amount):
		self.flagpoints += amount	
	def setflagtouches(self, amount = 0):
		self.flagtouches += 1
		self.flagpoints += amount
	def setbellflags(self, amount):
		self.bellflags += amount

	def setballpoints(self, amount):
		self.ballpoints += amount
	def setballtouches(self, amount = 0):
		self.balltouches += 1
		self.ballpoints += amount
	def setballtime(self, amount):
		self.balltime += amount	

	def totals(self):
		totals = self.killpoints + self.flagpoints + self.ballpoints
		return totals

def mm_attach(arena):

	arena.stats_saved_stats = []
	
	arena.stats_mystats = \
		asss.add_command("mystats", \
		mystats, \
		arena)
		
	arena.stats_playeraction = \
		asss.reg_callback(asss.CB_PLAYERACTION, \
		stats_playeraction, \
		arena)
		
	arena.stats_shipfreqchange = \
		asss.reg_callback(asss.CB_SHIPFREQCHANGE, \
		stats_shipfreqchange, \
		arena)
	
def mm_detach(arena):
	for attr in [
		'stats_mystats',
		'stats_saved_stats',
		'stats_playeraction',
		'stats_shipfreqchange']:
		try: delattr(arena, attr)
		except: pass
		
def search_for_saved_stats(p, trace):

	event = getPEvent(p.freq)
	ae = getattr(p.arena, event, None)
	
	gameId = 0 if not ae else ae.gameId
		
	for item in p.arena.stats_saved_stats:
		if item['name'] == p.name and \
			item['event'] == event and \
			item['gameId'] == gameId and \
			item['freq'] == p.freq:
			p.stats = stats(p.name, p.freq, event, gameId)
			
			for stat, val in item.iteritems():
				setattr(p.stats, stat, val)
				
			p.arena.stats_saved_stats.remove(item)
			
			dev(p, '%s [ SAVED STATS RESTORED ]' %trace)
			return
			
	dev(p, '%s [ SAVED STATS NOT FOUND - CREATED NEW STATS ]' %trace)
	
	if event != 'None':
		p.stats = stats(p.name, p.freq, event, gameId)

def save_stats(p, trace):
	attrs = vars(p.stats)
	if hasattr(p, 'stats'):
		if p.stats.flagtouches > 1:
			p.arena.stats_saved_stats.append(attrs)
			delattr(p, 'stats')
			dev(p, '%s [ PLAYER STAT SHEET MOVED TO SAVES ]' %trace)
		else:
			dev(p, '%s [ PLAYER STAT SHEET BLANK: DELETED ]' %trace)
			delattr(p, 'stats')
	else:
		dev(p, '%s [ ERROR PLAYER HAD NO STAT SHEET ]' %trace)

def stats_playeraction(p, action, arena):
	if action == asss.PA_ENTERGAME:
		if p.freq != p.arena.specfreq:
			search_for_saved_stats(p, '[ PLAYER ENTERED GAME FROM LOGIN ]')
	elif action == asss.PA_LEAVEARENA:
		if p.freq != p.arena.specfreq:
			save_stats(p, '[ PLAYER LEFT GAME FROM EXIT ARENA ]')

def stats_shipfreqchange(p, newship, oldship, newfreq, oldfreq):
	if oldship == asss.SHIP_SPEC \
		and oldfreq == p.arena.specfreq \
		and newship != asss.SHIP_SPEC \
		and newfreq != p.arena.specfreq:
		search_for_saved_stats(p, '[ PLAYER ENTERED GAME FROM SPEC ]')
	elif newship == asss.SHIP_SPEC \
		and newfreq == p.arena.specfreq \
		and oldship != asss.SHIP_SPEC \
		and oldfreq != p.arena.specfreq:
		save_stats(p, '[ PLAYER ENTER SPEC FROM GAME ]')
	elif newfreq != oldfreq:
		save_stats(p, '[ PLAYER SWITCHED FREQS ]')
		search_for_saved_stats(p, '[ PLAYER SWITCHED FREQS ]')

#---
		
def send_saved_stats(p):
	found = 0
	for stat in p.arena.stats_saved_stats:
		if stat['name'] == p.name:
		
			found = 1

			chat.SendMessage(p, 'Saved Stats')
			chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =')
			
			chat.SendMessage(p, ' PLAYER : %-19s : Kills: %-3s  Deaths: %-3s                    Kill Points : %4s  '% \
				(stat['name'],
				stat['kills'],
				stat['deaths'],
				stat['killpoints']))
				
			chat.SendMessage(p, '  EVENT : %-19s : Flag Touches: %-4s                         Flag Points : %4s  '% \
				(stat['event'],
				stat['flagtouches'],
				stat['flagpoints']))
				
			chat.SendMessage(p, '   FREQ : %-19s : Ball Grabs: %-2s   Time: %-4s  Goals: %-2s     Ball Points : %4s  '% \
				(stat['freq'],
				stat['balltouches'],
				stat['balltime'],
				stat['ballgoals'],
				stat['ballpoints']))
				
			chat.SendMessage(p, ' GameID : %-19s :                                                 Totals : %4s'% \
				(stat['gameId'],
				stat['killpoints'] + stat['flagpoints'] + stat['ballpoints']))
				
			chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =')
	
	if found == 0:
		chat.SendMessage(p, 'Saved stats not found.')
	
		
def send_stats(p, i):
	if hasattr(i, 'stats'):
		chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =')
		
		chat.SendMessage(p, ' PLAYER : %-19s : Kills: %-3s  Deaths: %-3s                    Kill Points : %4s  '% \
			(i.stats.name,
			i.stats.kills,
			i.stats.deaths,
			i.stats.killpoints))
			
		chat.SendMessage(p, '  EVENT : %-19s : Flag Touches: %-4s                         Flag Points : %4s  '% \
			(i.stats.event,
			i.stats.flagtouches,
			i.stats.flagpoints))
			
		chat.SendMessage(p, '   FREQ : %-19s : Ball Grabs: %-2s   Time: %-4s  Goals: %-2s     Ball Points : %4s  '% \
			(i.stats.freq,
			i.stats.balltouches,
			i.stats.balltime,
			i.stats.ballgoals,
			i.stats.ballpoints))
			
		chat.SendMessage(p, ' GameID : %-19s :                                                 Totals : %4s'% \
			(i.stats.gameId,
			i.stats.totals()))
			
		chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =')
	else: chat.SendMessage(p, 'Current stats not found. Try: ?mystats <saves>')

def mystats(cmd, params, p, arena):
# help text (?help mystats)
	"""\
Module: <py> pub_stats
Params: Saves, <Name>, <Event>
"""
	if not params:
		send_stats(p, p)
	elif params.lower() == 'all':
		player = [p]
		def findplayer(p):
			send_stats(player[0], p)
		asss.for_each_player(findplayer)
		
	elif params.capitalize() in EventMap.values():
		player = [p]
		found = [False]
		def findplayer(p):
			if hasattr(p, 'stats'):
				if p.stats.event.lower() == params.lower():
					found[0] = [True]
					send_stats(player[0], p)
		asss.for_each_player(findplayer)
		if not found[0]:
			chat.SendMessage(p, '%s event has no current stats.' %params.capitalize())
	elif params and params == 'saves':
		send_saved_stats(p)
	elif params:
		player = [p]
		found = [False]
		hasstats = [False]
		def findplayer(p):
			if p.name.lower() == params.lower():
				found[0] = [True]
				if hasattr(p, 'stats'):
					hasstats[0] = [True]
					send_stats(player[0], p)
		asss.for_each_player(findplayer)
		
		if not found[0]:
			chat.SendMessage(p, 'Player: %s was not found. Use: ?mystats %stickname' %(params,'%'))
		elif found[0] and not hasstats[0]:
			chat.SendMessage(p, 'Player: %s has no current stats, try checking. ?savedstats <name>' %params)

def allstats(p):
	if not params:
		chat.SendMessage(p, '?allstats <everything> - Displays stats for all events.')
		chat.SendMessage(p, '?allstats <eventname> - Displays stats for <eventname>.')
	elif params.lower() == 'everything':
		pass

	elif params.lower() == 'everything':
		pass
		
