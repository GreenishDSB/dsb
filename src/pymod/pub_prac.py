###################################################################
# Module: pub_prac.py                                      By: Fly
# Event Name: Practice
# Prefix: prac_
# Freqs: 2, 3
###################################################################
# Notes: 
#
#
###################################################################

from pub_stats import *

event = 'prac'
eventname = 'Practice'
eventfreqs = [2,3]
gameID = 0
prefix = 'prac_'

minplayers = 4
maxplayers = 12

callbacks = ['CB_TURFTAG','CB_KILL']

###################################################################

def event_setup(arena):
	if not hasattr(arena, event):
		setattr(arena, event, \
			events(event, eventname, \
			eventfreqs, gameID, arena))
			
def setstat(p, stat, amount):
	if hasattr(p, 'stats'):
		setattr(p.stats, stat, amount)
	else: 
		dev(arena, 'ERROR: Module: %s; Function: setstat' %eventname)

def CB_TURFTAG(arena, p, fid, oldfreq, newfreq):
	if p.stats.event == event:
		p.stats.setflagtouches(10)

def CB_KILL(arena, p, k, bty, flags, pts, green):
	if p.stats.event == event:
		p.stats.setkills(100)
		k.stats.setdeaths(0)

def CB_BALLPICKUP(arena, p, bid):
	if p.stats.event == event:
		p.stats.setballtouches(100)

def prefixed(item):
	return ''.join([prefix, item])
	
def mm_attach(arena):

	setattr(arena, prefixed('controls'), \
		asss.add_command(event, eval('controls'), arena))

	for callback in callbacks:
		setattr(arena, prefixed(callback), \
			asss.reg_callback(getattr(asss, callback), \
			eval(callback), arena)) 
	event_setup(arena)
	
def mm_detach(arena):

	for item in callbacks:
		try: delattr(arena, prefixed(item))
		except: pass
	
	for attr in [event, prefixed('controls')]:
		try: delattr(arena, attr)
		except: pass
	
#----------------------------------------------------------------------------------------------
# gamestates: idle, pregame, running, paused, postgame
# commands: ?<event> <param> params: setup, start, pause, resume, end, endsave, kill
	
def controls(cmd, params, p, arena):
	
	if not hasattr(arena, event):
		event_setup(arena)
			
	elif hasattr(arena, event):
		if params:
		
			params = params.lower()
			
			ae = getattr(arena, event)
			ev = ae.event
			evc = ev.capitalize()
			en = ae.eventname
			gi = ae.gameId
			gs = ae.gamestate
			ef = ae.eventfreqs
			
			if params == 'setup':
				if gs in ['idle']:
					pass
			elif params == 'start':
				if gs in ['pregame']:
					pass
			elif params == 'pause':
				if gs in ['running']:
					pass
			elif params == 'resume':
				if gs in ['paused']:
					pass
			elif params == 'end':
				if gs in ['running', 'paused', 'postgame']:
					pass
			elif params == 'endsave':
				if gs in ['postgame']:
					pass
			elif params == 'kill':
				if gs in ['idle', 'pregame', 'running', 'paused', 'postgame']:
					eventKill(arena)
				
		else: showOptions(p)
		
def eventSetup():
	pass

def eventStart():
	pass

def eventPause():
	pass

def eventResume():
	pass
	
def eventEnd():
	pass
	
def eventEndSave():
	pass
	
def eventKill(arena):
	ae = getattr(arena, event)
	ae.kill()
	
def showOptions(p):

	if hasattr(p.arena, event):
		ae = getattr(p.arena, event)
		ev = ae.event
		evc = ev.capitalize()
		en = ae.eventname
		gi = ae.gameId
		gs = ae.gamestate
		ef = ae.eventfreqs
		
		chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = =')
		str = 'Event: {}'.format(evc)
		chat.SendMessage(p, 'Event Name: {0:19} {1:>19}'.format(en, str))
		str = 'Freqs: {}'.format(ef)
		chat.SendMessage(p, 'Game State: {0:19} {1:>19}'.format(gs, str))
		chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = =')
		
		# setup, start, pause, resume, end, endsave, kill
		# idle, pregame, running, paused, postgame
		
		if gs == 'idle': chat.SendMessage(p, 'Command options: ?{0} <spam>, ?{0} <setup>'.format(ev))
		elif gs == 'pregame': chat.SendMessage(p, 'Command options: ?{0} <spam>, ?{0} <start>'.format(ev))
		elif gs == 'running': chat.SendMessage(p, 'Command options: ?{0} <pause>, ?{0} <kill>'.format(ev))
		elif gs == 'paused': chat.SendMessage(p, 'Command options: ?{0} <resume>, ?{0} <kill>'.format(ev))
		elif gs == 'postgame': chat.SendMessage(p, 'Command options: ?{0} <end>, ?{0} <endsave>'.format(ev))
	else: chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = =')
