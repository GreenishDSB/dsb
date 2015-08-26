###################################################################
# Module: pub_join.py By: Fly
# Prefix: join
#
###################################################################
# Notes:
#
# Creates the list for ?join <event>, supports is for all events in
# one list.
#
# I was workin on this at 3am and just shutdown where i was and havent
# returned to it since.
#
# arena.waitlist[
# ('prac', 'Fly Swatter'),
# ('soccer', 'Fly Swatter'),
# ('bab', 'some player')]
# etc..
#
###################################################################
from pub_lib import *
chat = asss.get_interface(asss.I_CHAT)
eventlist = ['prac', 'duel', 'bab', 'soccer']
def joinlist(cmd, params, p, arena):
#dev(p,'waitlist: %s' %arena.waitlist)
if not params:
chat.SendMessage(p, '?Join <event>, events: prac, duel, bab, soccer.')
return
elif not params.lower() in eventlist:
chat.SendMessage(p, '?Join <event>, events: prac, duel, bab, soccer.')
return
else:
params = params.lower()
count = 0
found = False
for j in arena.waitlist:
if j[0] == params:
count +=1
if j[0] == params and j[1] == p.name:
found = True
arena.waitlist.remove(j)
chat.SendMessage(p, 'You have been removed from the %s list.' %params )
break
if not found:
arena.waitlist.append((params, p.name))
chat.SendMessage(p, 'You have been added to the %s list.' %params)
for j in arena.waitlist:
if j[0] == params:
str = ''
str += j[1] + ', '
str = str[:-2]
chat.SendMessage(p, 'Players on %s: %s' %(params, str))
def mm_attach(arena):
arena.waitlist = []
arena.join = asss.add_command("join", joinlist, arena)
def mm_detach(arena):
for attr in ['join', 'waitlist']:
try: delattr(arena, attr)
except: pass
