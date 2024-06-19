import machine
import BlackBox_pkg.sdcard as sdcard
import uos
import json

class SDCard:
    #---------------------------------------------------------------------------------------------------------------------------------
    # Read and Write Wifi Password and SSID JSON
    def read_password_file(self):
        try:
            CS = machine.Pin(9, machine.Pin.OUT)
            spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(8))

            sd = sdcard.SDCard(spi,CS)

            vfs = uos.VfsFat(sd)
            uos.mount(vfs, "/sd")

            def SDcard():
                my_data = {
                    "WiFi": {"ssid": "Phone", "password": "sakib dalal"}
                }

                # Writing into json file
                with open("/sd/network.json", "w") as json_file:
                    json.dump(my_data, json_file)
                
                # Open the file we just created and read from it
                with open("/sd/network.json", "r") as file:
                    print("Reading network.json...")
                    data = json.load(file)
                    print(data)
                return (data, True)

            if SDcard():
                print("SD CARD PRESENT")
            else:
                print("NO SD CARD")

        except Exception as e:
            print("Error:", e)
            
    #---------------------------------------------------------------------------------------------------------------------------------
    # Text Files
    
    # Read Text File
    def read_text_file(self, file_name):
        file_path = f"/sd/{file_name}"
        with open(file_path, "r") as file:
            print(f"Reading file {file_name}")
            data = file.read()
            print(data)
            return data
        
    # Write Text File # if mode "w" then write, if mode "u" then update
    def write_text_file(self, file_name, mode, text):
        file_path = f"/sd/{file_name}"
        if mode == "w":
            with open(file_path, mode="w") as text_file:
                print(f"Writing text in {file_name}...")
                text_file.write(text)
                print(f"Done writing text in {file_name}...")

        elif mode == "u":
            with open(file_path, mode="a") as text_file:
                print(f"Updating text in {file_name}...")
                text_file.write(f"\n{text}")
                print(f"Done updating text in {file_name}...")
        else:
            print(f"Error in making {file_name}")
    #---------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    my_sdcard = SDCard()
    my_sdcard.read_password_file()
    my_sdcard.write_text_file(file_name="data.txt", mode="w", text="Hello World")
    my_sdcard.write_text_file(file_name="data.txt", mode="u", text="Update Hello World")
    my_sdcard.read_text_file(file_name="data.txt")