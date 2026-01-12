# Write your code here :-)
import board
import digitalio
import busio
import wifi
import time
import socketpool
import sys
import adafruit_requests
import ssl
import gifio
import storage
import sdcardio
import displayio
import adafruit_jd79661
from fourwire import FourWire

url = "https://radar.weather.gov/ridge/standard/CONUS_loop.gif"

#Engage LED light
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

#Test storage
vfs = storage.getmount("/")
if vfs.readonly:
    print("Filesystem is Read Only")
else:
    print("Filesystem is Writable")

#Initiate Screen
displayio.release_displays()
screenSPI = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
screenCS = board.GP14
screenDC = board.GP15
screen_reset = board.GP4
screen_busy = board.GP3
screen_enable = digitalio.DigitalInOut(board.GP27)
screen_enable.direction = digitalio.Direction.OUTPUT
print("displays released")
display_bus = FourWire(screenSPI, command=screenDC, chip_select=screenCS, reset=screen_reset, baudrate=1000000)
screen_enable.value = True
time.sleep(1)
print("display bus created")
display = adafruit_jd79661.JD79661(display_bus,width=250,height=122,busy_pin=screen_busy,rotation=270,colstart=0,highlight_color=0x00FF00,highlight_color2=0xFF0000)
print("display initialized")
display_group = displayio.Group()
print("display group created")
pic = displayio.OnDiskBitmap("/icon.bmp")
print("pic loaded")
display_tile = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
print("display_tile created")
display_group.append(display_tile)
display.root_group = display_group
display.refresh()
print("refreshed")
time.sleep(display.time_to_refresh + 2)
print("display initialization complete")
#Initiate SD card
sd = sdcardio.SDCard(screenSPI, board.GP20)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')
print("SD card:" + os.listdir('/sd'))

#initiate connection to wifi
radio = wifi.radio
print("Connecting...")
networks = radio.start_scanning_networks()

time.sleep(12)

radio.stop_scanning_networks()

print(networks)
home = ""
for network in networks:
    print(network.ssid)
    if (network.ssid == "fidium"):
        home = network
if (not home):
    print("Failed to discover to Fidium")
    led.value = False
    sys.exit(408)
print(home.bssid)
radio.connect(home.ssid,"zorritodarla")

time.sleep(5)

isConnected = radio.connected
print(isConnected)
if (not isConnected):
    print("Failed to connect to Fidium")
    led.value = False
    sys.exit(504)
pool = socketpool.SocketPool(radio)
print(pool)

#make request to HTTP to get radar gif
requests# Write your code here :-)
import board
import digitalio
import busio
import wifi
import time
import socketpool
import sys
import adafruit_requests
import ssl
import gifio
import storage
import sdcardio
import displayio
import adafruit_jd79661
from fourwire import FourWire

displayio.release_displays()
print("displays released")


#define variables
url = "https://radar.weather.gov/ridge/standard/CONUS_loop.gif"
screenSPI = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
screenCS = board.GP17
screenDC = board.GP15
screen_reset = board.GP4
screen_busy = board.GP3
screen_enable = digitalio.DigitalInOut(board.GP22)
screen_enable.direction = digitalio.Direction.OUTPUT
screen_enable.value = True

#Engage LED light
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

#Test storage
vfs = storage.getmount("/")
if vfs.readonly:
    print("Filesystem is Read Only")
else:
    print("Filesystem is Writable")

#Initiate SD card
sd = sdcardio.SDCard(screenSPI, board.GP20)
print("sd card object created")
vfs = storage.VfsFat(sd)
print("VFS storage enabled")
storage.mount(vfs, '/sd')
#print("SD Card mounted")
print("SD card:" + os.listdir('/sd'))

#Initiate Screen

display_bus = FourWire(screenSPI, command=screenDC, chip_select=screenCS, reset=screen_reset, baudrate=1000000)
time.sleep(1)
print("display bus created")
display = adafruit_jd79661.JD79661(display_bus,width=250,height=122,busy_pin=screen_busy,rotation=270,colstart=0,highlight_color=0x00FF00,highlight_color2=0xFF0000)
print("display initialized")
display_group = displayio.Group()
print("display group created")
pic = displayio.OnDiskBitmap("/display-ruler-640x360.bmp")
print("pic loaded")
display_tile = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
print("display_tile created")
display_group.append(display_tile)
display.root_group = display_group
display.refresh()
print("refreshed")
time.sleep(display.time_to_refresh + 2)
print("display initialization complete")


#initiate connection to wifi
radio = wifi.radio
print("Connecting...")
networks = radio.start_scanning_networks()

time.sleep(12)

radio.stop_scanning_networks()

print(networks)
home = ""
for network in networks:
    print(network.ssid)
    if (network.ssid == "fidium"):
        home = network
if (not home):
    print("Failed to discover to Fidium")
    led.value = False
    sys.exit(408)
print(home.bssid)
radio.connect(home.ssid,"zorritodarla")

time.sleep(5)

isConnected = radio.connected
print(isConnected)
if (not isConnected):
    print("Failed to connect to Fidium")
    led.value = False
    sys.exit(504)
pool = socketpool.SocketPool(radio)
print(pool)

#make request to HTTP to get radar gif
requests = adafruit_requests.Session(pool, ssl.create_default_context())


while True:
    try:
        print("requests.get()", end="")
        response = requests.get(url, stream=True)  # Enable streaming mode
        print(" - success")
        break
    except OSError as err:
        print(" - failed! retry in 1 second")
        print("OSError:", err)
        time.sleep(1)

#save radar gif
image_path="/sd/radar.gif"
print("Save to", image_path)

with open(image_path, "wb") as file:
    for chunk in response.iter_content(1024):  # Download in chunks of 1024 bytes
        file.write(chunk)

print("Saved")

file.close()


#Disable LED Light and close connections
response.close()
led.value = False
screen_enable.value = False = adafruit_requests.Session(pool, ssl.create_default_context())


while True:
    try:
        print("requests.get()", end="")
        response = requests.get(url, stream=True)  # Enable streaming mode
        print(" - success")
        break
    except OSError as err:
        print(" - failed! retry in 1 second")
        print("OSError:", err)
        time.sleep(1)

#save radar gif
image_path="/sd/radar.gif"
print("Save to", image_path)

with open(image_path, "wb") as file:
    for chunk in response.iter_content(1024):  # Download in chunks of 1024 bytes
        file.write(chunk)

print("Saved")

file.close()


#Disable LED Light and close connections
response.close()
led.value = False
screen_enable.value = False
