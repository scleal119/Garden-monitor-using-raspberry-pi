
from signal import signal, SIGTERM, SIGHUP, pause
import RPi.GPIO as GPIO
import time
import sys
from smbus import SMBus
from rpi_lcd import LCD
import dht11

# Define the GPIO pins for the moisture sensor and DHT11 sensor
moisture_channel = 21
dht11_pin = 4

# Define the I2C address for the LCD screen
lcd_address = 0x27
lcd_bus = 1

# Define the LCD screen dimensions
lcd_width = 16
lcd_rows = 2

# Initialize the GPIO pins and LCD screen
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_channel, GPIO.IN)
lcd = LCD(lcd_address, lcd_bus, lcd_width, lcd_rows)

# Initialize the DHT11 sensor
dht11_sensor = dht11.DHT11(pin=dht11_pin)

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def c_to_f(celsius):
	fahrenheit=celsius*9/5 +32
	return fahrenheit

# Loop to continuously read the moisture sensor and output to the LCD screen
def callback(channel):
    # Read the moisture sensor data
    moisture = GPIO.input(channel)
    if moisture:
        lcd.text('WATER FOUND!', 1)
    else:
        lcd.text('NO WATER!', 1)

GPIO.add_event_detect(moisture_channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(moisture_channel, callback)

# Wait for some time before reading again
display_temp = True
while True:
	result = dht11_sensor.read()
	if result.is_valid():
		if display_temp:
			fahrenheit=c_to_f(result.temperature)
			lcd.text('Temp: {}F'.format(fahrenheit), 2)
		else:
			lcd.text('Humidity: {}%'.format(result.humidity), 2)
		display_temp = not display_temp
	else:
		lcd.text('Loading...', 2)

	time.sleep(2)
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    sys.exit(0)

