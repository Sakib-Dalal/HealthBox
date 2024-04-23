from machine import Pin
import time

led = Pin(2, Pin.OUT)

# Blink Function
def blink():
    while True:
        print("LED ON")
        led.value(0)
        time.sleep(1)
        print("LED OFF")
        led.value(1)
        time.sleep(1)

# Calling blink function
blink()