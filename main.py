import hue
from deep_sleep import deep_sleep
from config import deep_sleep_time, off_time, on_time, light_group

from machine import Pin, SoftI2C
import tsl2561
from rtc import read_time_from_rtc
from send import send_log_message_to_queue

i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
lux = tsl2561.TSL2561(i2c=i2c)

light_value = int(lux.read())

h = hue.Bridge()

# time.sleep(30)


def get_group_number(group=light_group):
    groups = h.getGroups()
    sofa = {i for i in groups if groups[i] == group}
    return list(sofa)[0]


def is_between(time_check, time_range):
    if time_range[1] < time_range[0]:
        return time_check >= time_range[0] or time_check <= time_range[1]
    else:
        return time_range[0] <= time_check <= time_range[1]


def set_brightness_level(brightness_value):
    if not group_status:
        h.setGroup(group_number, bri=brightness_value, on=True)
    current_brightness = group_info["action"]["bri"]
    if not current_brightness == brightness_value:
        h.setGroup(group_number, bri=brightness_value, on=True)
        print("Setting Light Value to {}".format(brightness_value))
    else:
        print("Lights already set to {}, doing nothing".format(brightness_value))


group_number = get_group_number(group=light_group)
group_info = h.getGroup(group_number)
group_status = group_info["state"]["any_on"]


current_time = read_time_from_rtc()

if is_between(current_time, (on_time, off_time)):
    send_log_message_to_queue("Current time is {}, this is between {} and {}, light value is {}".format(
        current_time, on_time, off_time, light_value))
    if light_value > 10:
        if group_status:
            h.setGroup(group_number, on=False)

    if 7 <= light_value <= 10:
        target_brightness_value = 128
        set_brightness_level(target_brightness_value)

    if 4 <= light_value <= 6:
        target_brightness_value = 192
        set_brightness_level(target_brightness_value)

    if 0 <= light_value <= 3:
        target_brightness_value = 254
        set_brightness_level(target_brightness_value)
else:
    send_log_message_to_queue("Current time is {}, this is not between {} and {}, light value is {}".format(
        current_time, on_time, off_time, light_value))
    if group_status:
        print("Lights are ON Current time is {}".format(current_time))
        h.setGroup(group_number, on=False)
        print("Turning off Lights")

deep_sleep(deep_sleep_time)
