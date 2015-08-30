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
		reset_event_player_stats(self.arena, self.event)
		self.gamestate = 'running'
		self.gameId += 1
		
	def kill(self):
		self.gamestate = 'idle'
		reset_event_player_stats(self.arena, self.event)
		#chat.SendArenaMessage(self.arena, '{} terminated.'.format(self.eventname))
		
		def each_player(p):
			if hasattr(p, 'stats'):
				if p.stats.event == self.event:
					chat.SendMessage(p, '{} terminated.'.format(self.eventname))
					game.SetShipAndFreq(p, 8, 69)
		asss.for_each_player(each_player)

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
		self.deaths += 1
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

	def setballgoals(self, amount = 0):
		self.ballgoals += 1
		self.ballpoints += amount
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

def make_new_player_stats(p):
	event = get_event(p.freq)
	ae = getattr(p.arena, event, None)
	gameId = 0 if not ae else ae.gameId	
	p.stats = stats(p.name, p.freq, event, gameId)
		
def reset_event_player_stats(arena, event):
	for _p in arena.stats_saves:
		if _p['event'] == event:
			arena.stats_saves.remove(_p)	
	def each_player(p):
		if hasattr(p, 'stats'):
			if p.stats.event == event:
				delattr(p, 'stats')
				make_new_player_stats(p)
	asss.for_each_player(each_player)

def move_player_stats_to_saves(p, trace):
	if hasattr(p, 'stats'):
		if p.stats.totals() > 0:
			attrs = vars(p.stats)
			p.arena.stats_saves.append(attrs)
			delattr(p, 'stats')
			dev(p, '%s [PLAYER STAT SHEET MOVED TO SAVES]' %trace)
		else:
			delattr(p, 'stats')
			dev(p, '%s [PLAYER STAT SHEET BLANK: DELETED]' %trace)
	else: dev(p, '%s [ERROR PLAYER HAD NO STAT SHEET]' %trace)

def check_for_saved_stats(p):
	event = get_event(p.freq)
	ae = getattr(p.arena, event, None)
	gi = 0 if not ae else ae.gameId
	for item in p.arena.stats_saves:
		if item['name'] == p.name \
			and item['freq'] == p.freq \
			and item['event'] == event \
			and item['gameId'] == gi:
			return item
	return None

def restore_saved_stats_or_make_new(p, trace):

	p_saved_stats = check_for_saved_stats(p)
	
	if p_saved_stats:
		make_new_player_stats(p)
		for stat, val in p_saved_stats.iteritems():
			setattr(p.stats, stat, val)

		p.arena.stats_saves.remove(p_saved_stats)
		dev(p, '%s [SAVED STATS RESTORED]' %trace)
		return

	if get_event(p.freq):
		make_new_player_stats(p)
		dev(p, '%s [SAVED STATS NOT FOUND - CREATED NEW STATS]' %trace)

def mystats(cmd, params, p, arena):
	found = True
	if params:
		_p = getP(params)
		if not _p:
			found = False
	else: _p = p
	if found:
		if hasattr(p, 'stats'):
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
		else: chat.SendMessage(p, 'Player has no current stats.')
	else: chat.SendMessage(p, 'Player not found. ?mystats or ?mystats <name>')
	
def EVENT_PLAYER_ENTERED(p):
	restore_saved_stats_or_make_new(p, '[EVENT_PLAYER_ENTERED]')

def EVENT_PLAYER_EXITED(p):
	move_player_stats_to_saves(p, '[EVENT_PLAYER_EXITED]')

def EVENT_PLAYER_CHANGED_FREQS(p):
	move_player_stats_to_saves(p, '[EVENT_PLAYER_CHANGED_FREQS]')
	restore_saved_stats_or_make_new(p, '[EVENT_PLAYER_CHANGED_FREQS]')

def CB_PLAYERACTION(p, action, arena):
	if action == asss.PA_ENTERGAME:
		if p.freq != p.arena.specfreq:
			EVENT_PLAYER_ENTERED(p)
	elif action == asss.PA_LEAVEARENA:
		if p.freq != p.arena.specfreq:
			EVENT_PLAYER_EXITED(p)

def CB_SHIPFREQCHANGE(p, newship, oldship, newfreq, oldfreq):
	if oldship == asss.SHIP_SPEC \
		and oldfreq == p.arena.specfreq \
		and newship != asss.SHIP_SPEC \
		and newfreq != p.arena.specfreq:
		EVENT_PLAYER_ENTERED(p)
		
	elif newship == asss.SHIP_SPEC \
		and newfreq == p.arena.specfreq \
		and oldship != asss.SHIP_SPEC \
		and oldfreq != p.arena.specfreq:
		EVENT_PLAYER_EXITED(p)
		
	elif newfreq != oldfreq:
		EVENT_PLAYER_CHANGED_FREQS(p)
		
def mm_attach(arena):
	arena.stats_saves = []
	
	arena.stats_mystats = \
		asss.add_command("mystats", \
		mystats, \
		arena)
		
	arena.stats_CB_PLAYERACTION = \
		asss.reg_callback(asss.CB_PLAYERACTION, \
		CB_PLAYERACTION, \
		arena)
		
	arena.stats_CB_SHIPFREQCHANGE = \
		asss.reg_callback(asss.CB_SHIPFREQCHANGE, \
		CB_SHIPFREQCHANGE, \
		arena)

def mm_detach(arena):
	for attr in [
		'stats_mystats',
		'stats_saves',
		'stats_CB_PLAYERACTION',
		'stats_CB_SHIPFREQCHANGE',
		'stats_CB_PRESHIPFREQCHANGE']:
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
