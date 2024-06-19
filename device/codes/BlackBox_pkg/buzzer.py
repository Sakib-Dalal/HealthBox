from machine import Pin
import time

buzzer_pin = Pin(1, Pin.OUT)

# Buzzer Class
class Buzzer:
    # Turn buzzer On
    def buzzer_on(self):
        print("buzzer ON")
        buzzer_pin.value(1)
        time.sleep(1)

        
    # Turn buzzer Off
    def buzzer_off(self):
        print("buzzer OFF")
        buzzer_pin.value(0)
        time.sleep(1)
        
        
    # buzzer on for nth sec 
    def buzzer_time_on(self, n):
        print(f"buzzer ON FOR {n}sec")
        buzzer_pin.value(1)
        time.sleep(n)
        buzzer_pin.value(0)
        
        
    # Blink buzzer 1 sec On and 1 sec Off
    def blink_buzzer(self):
        self.buzzer_on()
        self.buzzer_off()
    
    
    # Blink buzzer fast
    def blink_buzzer_fast(self):
        print("buzzer ON")
        buzzer_pin.value(1)
        time.sleep(0.3)
        print("buzzer OFF")
        buzzer_pin.value(0)
        time.sleep(0.3)
    
    
    # blink nth time with speed control fast or slow
    def blink_buzzer_nth(self, num_blink, fast=False):
        self.count = num_blink
        self.status = fast
        for i in range(0, self.count):
            print(f"count {i+1}")
            if self.status:
                self.blink_buzzer_fast()
            else:
                self.blink_buzzer()

    
if __name__ == "__main__":
    my_buzzer = Buzzer()
    my_buzzer.buzzer_on()
    my_buzzer.buzzer_off()
    my_buzzer.blink_buzzer()
    my_buzzer.blink_buzzer_fast()

