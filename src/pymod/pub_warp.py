###################################################################
# Module: pub_warp.py                                      By: Fly
# Prefix: warp_            
###################################################################
# Notes: 
#
# Will need final rewite of this once things get figured out.
#
###################################################################

from pub_lib import *

import random

#--- auto warp for event freqs

def send_player_to_correct_safezone(p, trace):

	spawn = safezone_map.setdefault(p.freq, 'None')
	
	event = getPEvent(p.freq)
	ae = getattr(p.arena, event, None)
	
	if not spawn == 'None':
		if spawn[0] == 'point':
			x = spawn[1] 
			y = spawn[2]
		elif spawn[0] == 'box':
			x = random.randrange(spawn[1], spawn[2], 1)
			y = random.randrange(spawn[3], spawn[4], 1)
		elif spawn[0] == 'radius':
			x = random.randrange(spawn[1]-spawn[3], spawn[1]+spawn[3], 1)
			y = random.randrange(spawn[2]-spawn[3], spawn[2]+spawn[3], 1)
		game.WarpTo(p, x, y)

def innkz(x, y):
	if x > 7888 and x < 8496:
		if y > 7888 and y < 8480:
			return True
	return False

def autowarp(p, trace):
	send_player_to_correct_safezone(p, trace)

def spawn(p, type):
	autowarp(p, '[ EVENT: SPAWN ]')

def safezone(p, x, y, entering):
	if innkz(x, y):
		autowarp(p, '[ EVENT: SAFEZONE ]')

def warped(p, oldX, oldY, x, y):
	if innkz(x, y):
		autowarp(p, '[ EVENT: WARPED ]')

#--- ?ds below

def warpto_ds(arena, p):
	sections = [0,1,2,3,4,5]
	box = [ 
		[387,402,286,302], 
		[125,155,245,279], 
		[165,200,261,271], 
		[375,415,320,345], 
		[365,425,251,256], 
		[237,249,186,195]] 
	random.shuffle(sections)
	x = random.randrange(box[sections[0]][0], 
		box[sections[0]][1], 1)
	y = random.randrange(box[sections[0]][2], 
		box[sections[0]][3], 1)
	game.WarpTo(p, x, y)

def checks(p, arena):
	if p.arena == arena and \
		p.ship in range(0,8) and \
		p.type != asss.T_FAKE:
		return True
	return False

def setwarp(cmd, params, p, arena):
	if params:
		if params == "ds":
			if arena.warp_usewarp_ds:
				arena.warp_usewarp_ds = False
				chat.SendMessage(p, "The command ?ds is now unavailable.")
			else:
				arena.warp_usewarp_ds = True
				chat.SendMessage(p, "The command ?ds is now available.")
	else:
		chat.SendMessage(p, "Use: ?setwarp cmd, e.g. ?setwarp ds")
		
def ds(cmd, params, p, arena):
	if arena.warp_usewarp_ds:
		if checks(p, arena):
			if (p.position[6] == 160):
				warpto_ds(arena, p)
			else:
				chat.SendMessage(p, "Command available from a safety tile.")
	else:
		chat.SendMessage(p, "Command currently disabled.")
		
###################################################################
# CB_REGION not available for py.

def mm_attach(arena):
	arena.warp_spawn = asss.reg_callback(asss.CB_SPAWN, spawn, arena)
	arena.warp_safezone = asss.reg_callback(asss.CB_SAFEZONE, safezone, arena)
	arena.warp_warped = asss.reg_callback(asss.CB_WARP, warped, arena)
	
	arena.warp_usewarp_ds = True
	arena.warp_setwarp = asss.add_command("setwarp", setwarp, arena)
	arena.warp_ds = asss.add_command("ds", ds, arena)

def mm_detach(arena):
	for attr in ['warp_spawn', 'warp_safezone', 'warp_warped', \
		'warp_usewarp_ds', 'warp_setwarp', 'warp_ds']:
		try: delattr(arena, attr)
		except: pass
		
###################################################################
