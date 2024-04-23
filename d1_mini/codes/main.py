from machine import Pin
import network
import time

WIFI_SSID = "Phone"
WIFI_PASS = "sakib dalal"

led = Pin(2, Pin.OUT)

wifi = network.WLAN(network.STA_IF)

wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)

while not wifi.isconnected():
    print("Connecting")
    led.value(1)
    time.sleep(1)
    led.value(0)
    
led.value(1)
print(f"Connected to: {wifi.ifconfig()}")
    