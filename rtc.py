from machine import I2C, Pin

import urtc_driver

i2c = I2C(scl=Pin(5), sda=Pin(4))
rtc = urtc_driver.DS1307(i2c)


def read_time_from_rtc():
    datetime = rtc.datetime()

    return "{}:{}".format(add_leading_zero_if_required(datetime.hour), add_leading_zero_if_required(datetime.minute))


def add_leading_zero_if_required(datetime):
    if datetime < 10:
        return "0" + str(datetime)
    else:
        return datetime
