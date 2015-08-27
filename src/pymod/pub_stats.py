###################################################################
# Module: pub_stats.py                                     By: Fly
# Prefix: stats_
###################################################################
# Notes: 
# 
# 
# 
# 
###################################################################

from pub_lib import *

class events:
	def __init__(self, event, eventname, eventfreqs, gameId, arena):
		self.arena = arena
		self.event = event
		self.eventname = eventname
		self.eventfreqs = eventfreqs
		self.gameId = gameId
		self.gamestate = 'idle'
		
	def pregame(self):
		self.gamestate = 'pregame'
		
	def start(self):
		resetEventPlayerStats(self.arena, self.event)
		self.gamestate = 'running'
		self.gameId += 1
		
	def kill(self):
		self.gamestate = 'idle'
		resetEventPlayerStats(self.arena, self.event)

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

def newPlayerStats(p):
	event = getPEvent(p.freq)
	ae = getattr(p.arena, event, None)
	gameId = 0 if not ae else ae.gameId	
	p.stats = stats(p.name, p.freq, event, gameId)
		
def resetEventPlayerStats(arena, event):
	for _p in arena.stats_saves:
		if _p['event'] == event:
			arena.stats_saves.remove(_p)	
	def each_player(p):
		if hasattr(p, 'stats'):
			if p.stats.event == event:
				delattr(p, 'stats')
				newPlayerStats(p)
	asss.for_each_player(each_player)

def movePlayerStatsToSaves(p, trace):
	attrs = vars(p.stats)
	if hasattr(p, 'stats'):
		if p.stats.totals() > 0:
			p.arena.stats_saves.append(attrs)
			delattr(p, 'stats')
			dev(p, '%s [ PLAYER STAT SHEET MOVED TO SAVES ]' %trace)
		else:
			dev(p, '%s [ PLAYER STAT SHEET BLANK: DELETED ]' %trace)
			delattr(p, 'stats')
	else:
		dev(p, '%s [ ERROR PLAYER HAD NO STAT SHEET ]' %trace)

def restoreSavedStatsOrMakeNew(p, trace):

	event = getPEvent(p.freq)
	ae = getattr(p.arena, event, None)
	
	gameId = 0 if not ae else ae.gameId
		
	for item in p.arena.stats_saves:
		if item['name'] == p.name and \
			item['event'] == event and \
			item['gameId'] == gameId and \
			item['freq'] == p.freq:
			newPlayerStats(p)

			for stat, val in item.iteritems():
				setattr(p.stats, stat, val)

			p.arena.stats_saves.remove(item)

			dev(p, '%s [ SAVED STATS RESTORED ]' %trace)
			return

	dev(p, '%s [ SAVED STATS NOT FOUND - CREATED NEW STATS ]' %trace)

	if event != 'None':
		newPlayerStats(p)

def mystats(cmd, params, p, arena):
	found = True
	if params:
		_p = getP(params)
		if not _p:
			found = False
	else: _p = p
	if found:
		chat.SendMessage(p, 
		'{}({}), KD({}:{}:{}), Tk({}:{}), Flag({}:{}:{}), Ball({}:{}:{}:{}), Evt({}:{}), Total = {}'
		.format(
			_p.stats.name,
			_p.stats.freq,
			_p.stats.kills,
			_p.stats.deaths,
			_p.stats.killpoints,
			_p.stats.tks[0],
			_p.stats.tks[1],
			_p.stats.flagtouches,
			_p.stats.bellflags,
			_p.stats.flagpoints,
			_p.stats.balltouches,
			_p.stats.balltime,
			_p.stats.ballgoals,
			_p.stats.ballpoints,
			_p.stats.event,
			_p.stats.gameId,
			_p.stats.totals()))
	else: chat.SendMessage(p, 'Player not found. ?mystats or ?mystats <name>')
		
def stats_playeraction(p, action, arena):
	if action == asss.PA_ENTERGAME:
		if p.freq != p.arena.specfreq:
			restoreSavedStatsOrMakeNew(p, '[ PLAYER ENTERED GAME FROM LOGIN ]')
	elif action == asss.PA_LEAVEARENA:
		if p.freq != p.arena.specfreq:
			movePlayerStatsToSaves(p, '[ PLAYER LEFT GAME FROM EXIT ARENA ]')

def stats_shipfreqchange(p, newship, oldship, newfreq, oldfreq):
	if oldship == asss.SHIP_SPEC \
		and oldfreq == p.arena.specfreq \
		and newship != asss.SHIP_SPEC \
		and newfreq != p.arena.specfreq:
		restoreSavedStatsOrMakeNew(p, '[ PLAYER ENTERED GAME FROM SPEC ]')
	elif newship == asss.SHIP_SPEC \
		and newfreq == p.arena.specfreq \
		and oldship != asss.SHIP_SPEC \
		and oldfreq != p.arena.specfreq:
		movePlayerStatsToSaves(p, '[ PLAYER ENTER SPEC FROM GAME ]')
	elif newfreq != oldfreq:
		movePlayerStatsToSaves(p, '[ PLAYER SWITCHED FREQS ]')
		restoreSavedStatsOrMakeNew(p, '[ PLAYER SWITCHED FREQS ]')

def mm_attach(arena):
	arena.stats_saves = []
	
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
		'stats_saves',
		'stats_playeraction',
		'stats_shipfreqchange']:
		try: delattr(arena, attr)
		except: pass

#---

def eventStats(p, event):
	for _p in p.arena.stats_saves:
		if _p['event'] == event:
			str = ''
			for stat, val in _p.iteritems():
				str += '{}:{}, '.format(stat, val)
			chat.SendMessage(p, '{}'.format(str))
	def each_player(p):
		if hasattr(p, 'stats'):
			if p.stats.event == event:
				attrs = vars(p.stats)	
				str = ''
				for stat, val in attrs.iteritems():
					str += '{}:{}, '.format(stat, val)
				chat.SendMessage(p, '{}'.format(str))
	asss.for_each_player(each_player)
