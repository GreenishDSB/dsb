from asss import *
chat = get_interface(I_CHAT)
game = get_interface(I_GAME)

def StartTimer(cmd_str, param_str, player, arena):
    def tick():
       chat.SendArenaMessage(arena, str(arena.countdown_duration_s))
       arena.countdown_duration_s = arena.countdown_duration_s - arena.countdown_precision_ms / 1000.0
       if arena.countdown_duration_s <= 0:
          chat.SendArenaMessage(arena, "Time is up")
          arena.countdown_timer = None
    duration_s = int()
    try:
        duration_s = int(param_str)
    except:
        chat.SendMessage(player, param_str + ' is an invalid parameter')
        chat.SendMessage(player, 'usage ?purple <seconds>, e.g. ?purple 100')
        return
    duration_s = int(param_str)
    precision_ms = 100
    timer = set_timer(tick, 0, precision_ms / 10)
    arena.countdown_timer = timer
    arena.countdown_duration_s = duration_s
    arena.countdown_precision_ms = precision_ms
  
cmd1 = add_command("purple", StartTimer)

