from machine import Pin
import time

led_pin = Pin(2, Pin.OUT)

# LED Class
class LED:
    # Turn LED On
    def led_on(self):
        print("LED ON")
        led_pin.value(0)
        time.sleep(1)

        
    # Turn LEF Off
    def led_off(self):
        print("LED OFF")
        led_pin.value(1)
        time.sleep(1)
        
        
    # led on for nth sec 
    def led_time_on(self, n):
        print(f"LED ON FOR {n}sec")
        led_pin.value(0)
        time.sleep(n)
        led_pin.value(1)
        
        
    # Blink led 1 sec On and 1 sec Off
    def blink_led(self):
        self.led_on()
        self.led_off()
    
    
    # Blink led fast
    def blink_led_fast(self):
        print("LED ON")
        led_pin.value(0)
        time.sleep(0.3)
        print("LED OFF")
        led_pin.value(1)
        time.sleep(0.3)
    
    
    # blink nth time with speed control fast or slow
    def blink_led_nth(self, num_blink, fast=False):
        self.count = num_blink
        self.status = fast
        for i in range(0, self.count):
            print(f"count {i+1}")
            if self.status:
                self.blink_led_fast()
            else:
                self.blink_led()

    
if __name__ == "__main__":
    my_led = LED()
    my_led.led_on()
    my_led.led_off()
    my_led.blink_led()
    my_led.blink_led_fast()
