from config import is_configured_file, password, ssid
import network
import esp
import gc
from machine import Pin

led = Pin(2, Pin.OUT)

esp.osdebug(None)
gc.collect()

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('\n\nConnecting to network...')
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass

    print('Connected to network!!')


f = open(is_configured_file, "r")
is_configured_file_value = f.read()
f.close()

print("is_configured_file_value is {}".format(is_configured_file_value))
if is_configured_file_value == "False":
    print("Setting up RTC module")
    import ntptime
    ntptime.settime()

    from machine import I2C, Pin

    import urtc_driver
    from utime import localtime

    i2c = I2C(scl=Pin(5), sda=Pin(4))
    rtc = urtc_driver.DS1307(i2c)
    lt = localtime()
    rtc.datetime((lt[0], lt[1], lt[2], None, lt[3] + 2, lt[4], lt[5], lt[6]))

    import upip

    upip.install("micropython-umqtt.simple")

    f = open(is_configured_file, "w")
    f.write("True")
    f.close()
