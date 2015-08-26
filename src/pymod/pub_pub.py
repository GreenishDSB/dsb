###################################################################
# Module: pub_pub.py                                       By: Fly
# Event Name: Public
# Prefix: pub_
# Freqs: 6, 7
###################################################################
# Notes: 
#
#
###################################################################

from pub_stats import *

event = 'pub'
eventname = 'Public'
eventfreqs = [0,1]
gameID = 0
prefix = 'pub_'

callbacks = ['CB_TURFTAG','CB_KILL']

###################################################################

def event_setup(arena):
	if not hasattr(arena, event):
		setattr(arena, event, \
			events(event, eventname, \
			eventfreqs, gameID))
			
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
#----------------------------------------------------------------------------------------------

def controls(cmd, params, p, arena):
	
	if not hasattr(arena, event):
		event_setup(arena)
			
	elif hasattr(arena, event):
		ae = getattr(arena, event)
		ev = ae.event
		evc = ev.capitalize()
		en = ae.eventname
		gi = ae.gameId
		gs = ae.gamestate
		ef = ae.eventfreqs
		
		if not params:
			chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = =')
			str = 'Event: {}'.format(evc)
			chat.SendMessage(p, 'Event Name: {0:19} {1:>19}'.format(en, str))
			str = 'Freqs: {}'.format(ef)
			chat.SendMessage(p, 'Game State: {0:19} {1:>19}'.format(gs, str))
			chat.SendMessage(p, '= = = = = = = = = = = = = = = = = = = = = = = = = =')
			
			# idle, pregame, running, paused, postgame
			
			if gs == 'idle': chat.SendMessage(p, 'Command options: ?{0} <spam>, ?{0} <setup>'.format(ev))
			elif gs == 'pregame': chat.SendMessage(p, 'Command options: ?{0} <spam>, ?{0} <start>'.format(ev))
			elif gs == 'running': pass
			elif gs == 'paused': pass
			elif gs == 'postgame': pass
			
		else:
			params = params.lower()
			
			if params == 'kill':
				ae.kill()
				chat.SendMessage(p, 'kill() called. ')
				return
				
			# setup, start, pause, resume, end, endsave, kill
			
			if gs == 'idle':
				if params == 'setup':
					ae.pregame()
					chat.SendMessage(p, 'pregame() called.')
				elif params == 'spam':
					chat.SendArenaMessage(arena, 'Players needed for {}, use: ?join {}'.format(evc,ev))
					# send dsb chat ch
				else:
					chat.SendMessage(p, 'Please choose from the options.')

			elif gs == 'pregame':
				if params == 'start':
					ae.start()
					chat.SendMessage(p, 'start() called.')
				elif params == 'spam':
					chat.SendArenaMessage(arena, 'Players still needed for {}, use: ?join {}'.format(evc,ev))
					# send dsb chat ch
				else:
					chat.SendMessage(p, 'Please choose from the options.')
			
			elif gs == 'running': pass
			elif gs == 'paused': pass
			elif gs == 'postgame': pass
