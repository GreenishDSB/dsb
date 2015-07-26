from asss import *
chat = get_interface(I_CHAT)
game = get_interface(I_GAME)

def StartTimer(cmd_str, param_str, player, arena):
    class TimerMessage():
	def __init__(self, time, str):
            self.time = time
            self.str = str
            self.triggered = False
    messages = [ TimerMessage(30, "Get Ready! Starting in 30 Seconds."),\
                 TimerMessage(10, "Starting in 10 seconds."),\
                 TimerMessage(3 , "3"),\
                 TimerMessage(2 , "2"),\
                 TimerMessage(1 , "1"),\
                 TimerMessage(0 , "GO GO GO GO!") ]
    def tick():
        for message in messages:
            if message.triggered == False and arena.countdown_duration_s <= message.time:
                chat.SendArenaMessage(arena, message.str)
                message.triggered = True
        arena.countdown_duration_s = arena.countdown_duration_s - arena.countdown_precision_ms / 1000.0
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
  
cmd1 = add_command("start", StartTimer)

