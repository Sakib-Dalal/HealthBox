from machine import Pin
import network
import time

from BlackBox_pkg.led import LED

WIFI_SSID = "Phone"
WIFI_PASS = "sakib dalal"

class WiFi:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi_led = LED()


    # Connect to wifi
    def wifi_connect(self):
        self.wifi.active(True)
        self.wifi.connect(WIFI_SSID, WIFI_PASS)
        self.count = 0
    
        while not self.wifi.isconnected():
            print("Connecting to WiFi :)")
            self.wifi_led.blink_led()
            self.count += 1
            if self.count >= 10:
                print(f"Can't connect to network '{WIFI_SSID}'. Please try again!")
                self.wifi_led.blink_led_fast()
                self.wifi_led.led_off()
                break
            elif self.wifi.isconnected():
                print(f"Connected to: {self.wifi.ifconfig()}")
                self.wifi_led.blink_led_fast()
                self.wifi_led.led_time_on(n=5)


    # Diconnect from connected wifi
    def wifi_disconnect(self):
        self.wifi.disconnect()
        print(f"Disconnected Wifi from '{WIFI_SSID}' Succesfully!")
                
                
    # Print Status of the network
    def wifi_status(self):
        print(f"WiFi Connected: {self.wifi.isconnected()}")
        print(f"Connected to: {self.wifi.ifconfig()}")
        
        
    # Scans the available wifi's in your area
    def wifi_scan(self):
        print("(ssid, bssid, channel, RSSI, security, hidden)\n")
        networks = self.wifi.scan()
        print(networks)
        
if __name__ == "__main__":
    wifi = WiFi()
    wifi.wifi_scan()