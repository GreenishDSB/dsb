from asss import *

chat = get_interface(I_CHAT)

def arenaToPlayerList(arena):
    def each(player):
        if player.arena == arena:
            playerList.append(player)
    playerList = PlayerListType()
    for_each_player(each)
    return playerList

def c_purple(cmd, param, p, a):
    chat.SendAnyMessage(arenaToPlayerList(a), MSG_FUSCHIA, 0, p, param)

cmd1 = add_command("purple", c_purple)
