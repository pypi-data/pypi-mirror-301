# This file is placed in the Public Domain.


"uptime"


import time


from ..command  import STARTTIME, Commands
from ..persist import laps


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))


Commands.add(upt)
