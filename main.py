from network import WLAN
import pycom
from machine import UART, Pin, ADC, RTC
import machine
from LTR329ALS01 import LTR329ALS01
import ujson as json
import urequests as requests
import usocket as socket
import utime as time
import sock
from pysense import Pysense
import network
import gc


pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

# Connect to WIFI
print("STARTING WIFI")
wlan = network.WLAN(mode=network.WLAN.STA)

def connect_wifi():
    wlan.connect(ssid='weirdchamp', auth=(network.WLAN.WPA2, 'banana12'))
    start = time.time()
    while not wlan.isconnected():
        current = time.time()
        if(current > start+5 ):
            # Sometimes the wifi connection is stuck, try to connect again with recursive call
            connect_wifi()
        machine.idle()

connect_wifi()
print("CONNECTED")
pycom.rgbled(0xFF9900)

# Time is spaghetti
rtc = RTC()
rtc.ntp_sync("pool.ntp.org") #Sync the time hopefully

# Setup sensors
p_out = Pin('P19', mode=Pin.OUT)
p_out.value(1)
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P16

py = Pysense()
lt = LTR329ALS01(pysense = py, integration = LTR329ALS01.ALS_INT_50, rate = LTR329ALS01.ALS_RATE_500, gain = LTR329ALS01.ALS_GAIN_48X)

time.sleep(2)
real_time_in_milli = time.time() * 1000
zero_time = time.ticks_ms()


def get_data():
    truuuu_time = real_time_in_milli + time.ticks_ms() - zero_time
    light_level = lt.light()[0]
    temp = (apin.voltage() - 500) / 10
    #sent_time = time.time() * 1000
    data = "%s,%s,%s,%s" % (str(i), str(temp), str(light_level), str(truuuu_time))
    print(data)
    return data


s = sock.create_socket()
i = 0

# # # # # # # # # # # # # #
#   stuff for buffering   #
#    is commented out     #
# # # # # # # # # # # # # #
#buffer_string = ""
#data_buffer = list()
#start = time.time()

while True:
    #current = time.time() #elapsed time was to be used for buffering
    # light_level = lt.light()[0]
    # temp = (apin.voltage() - 500) / 10

    pycom.rgbled(0x020502) # I am green
    # sent_time = time.time()
    # data = "%s,%s,%s,%s" % (str(i), str(temp), str(light_level), str(sent_time))  

    if not wlan.isconnected(): # Always ensure internet is up before attempting to send
        pycom.rgbled(0xFF0000)
        connect_wifi()
    try: # try to send data
        data = get_data()
        
        # if len(data_buffer) > 0:
        #     temp = ""
        #     for item in data_buffer:
        #         temp += item + "\n"
        #     print("- - - - - - - - - - -")
        #     print(temp)
        #     print("- - - - - - - - - - -")
        #     s.send(temp)
        #     data_buffer = list()

        # # if(buffer_string != ""):
        # #     buffer_string = buffer_string + data
        # #     s.send(buffer_string)
        # #     buffer_string = ""
        # else:
        #     s.send(data)

        s.send(data)
    except Exception as e: # In case of socket error, try and make a new one
        #data_buffer.append(data)
        #buffer_string += data
        # print("- - - - - - - - - - -")
        # print(buffer_string)
        # print("- - - - - - - - - - -")
        # should buffer shit here
        # if current > start + 30:
        #     print("Trying to establish socket connection")
        #     start = time.time()
        pycom.rgbled(0xFF0000)
        s = sock.create_socket()

    i += 1
    time.sleep(0.5)
    gc.collect() # might need to garbage collect, not sure

