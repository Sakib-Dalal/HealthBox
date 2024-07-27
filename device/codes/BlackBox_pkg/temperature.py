import machine
import time

class Temperature:
    def __init__(self):
        self.temp_sensor = machine.ADC(4)
        self.ADC_voltage = None
        self.temperature_celcius = None
        self.temp_fahrenheit = None

    
    # method to read on board temperature sensor
    def read_temperature(self):
        self.ADC_voltage = self.temp_sensor.read_u16() * (3.3 / (65536))
        self.temperature_celcius = 27 - (self.ADC_voltage - 0.706)/0.001721
        self.temp_fahrenheit=32+(1.8*self.temperature_celcius)
        print("Temperature: {}°C {}°F".format(self.temperature_celcius,self.temp_fahrenheit))
        time.sleep_ms(500)
        return self.temperature_celcius, self.temp_fahrenheit

if __name__ == "__main__":
    my_pico_temp = Temperature()
    my_pico_temp.read_temperature()
    data = my_pico_temp.read_temperature()
    print(data)