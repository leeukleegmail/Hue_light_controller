import config
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
    sta_if.connect(config.ssid, config.password)
    while not sta_if.isconnected():
        pass

    print('Connected to network!!')
