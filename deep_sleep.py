
import machine


def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs)
    print('Going to sleep for {} seconds'.format(msecs/1000))
    machine.deepsleep()
