from asss import *

IMPERIAL_FREQ  = 0
REBEL_FREQ     = 1
IMPERIAL_SHIPS = [0, 1, 2, 3]
REBEL_SHIPS    = [4, 5, 6, 7]
SWITCH_SHIP    = [4, 5, 7, 6, 0, 1, 3, 2]

chat = get_interface(I_CHAT)
game = get_interface(I_GAME)

def enforce_legalships(p, newship, oldship, newfreq, oldfreq):
    if newfreq == IMPERIAL_FREQ and newship in REBEL_SHIPS:
        game.SetShip(p, SWITCH_SHIP[newship])
        chat.SendMessage(p, "You are a member of the Empire (Freq 0), and can only use ships 1,2,3,4")
    elif newfreq == REBEL_FREQ and newship in IMPERIAL_SHIPS:
        game.SetShip(p, SWITCH_SHIP[newship])
        chat.SendMessage(p, "You are a member of the Rebel Alliance (Freq 1), and can only use ships 5,6,7,8")

cb = reg_callback(CB_SHIPFREQCHANGE, enforce_legalships)
