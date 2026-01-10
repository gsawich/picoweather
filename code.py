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
image_path="/radar.gif"
print("Save to", image_path)

with open(image_path, "wb") as file:
    for chunk in response.iter_content(1024):  # Download in chunks of 1024 bytes
        file.write(chunk)

print("Saved")

file.close()


#Disable LED Light and close connections
response.close()
led.value = False
