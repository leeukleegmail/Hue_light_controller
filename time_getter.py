import ntptime
import time

# if needed, overwrite default time server
from config import time_offset

ntptime.host = "1.europe.pool.ntp.org"


def get_time():
    ntptime.settime()
    return {"years": time.localtime()[0], "month": time.localtime()[1], "day": time.localtime()[2],
            "hours": time.localtime()[3] + time_offset, "minutes": time.localtime()[4], "seconds": time.localtime()[5]}
