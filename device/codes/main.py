from machine import Pin
import network
import time
import _thread

from BlackBox_pkg.wifi_network import WiFi

wifi = WiFi()
wifi.wifi_connect()
wifi.wifi_status()
wifi.wifi_disconnect()
