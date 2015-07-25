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

# note: add cmd_moo to conf/groupdef.dir/default so players have permission to
#       use this command. After this is done, the server may or may not need 
#       to be recycled.
