#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
from Adafruit_BME280 import *
import lib.oled.SSD1331 as SSD1331

# Initialize the OLED display
disp = SSD1331.SSD1331()
disp.Init()
disp.clear()

# Initialize BME280 sensor
sensor = BME280(mode=BME280_OSAMPLE_8)

# Load fonts and images for pictograms
fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 18)
fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 12)
temp_icon = Image.open('./lib/oled/temp_icon.png')  # 16x16 icon for temperature
pressure_icon = Image.open('./lib/oled/pressure_icon.png')  # 16x16 icon for pressure
humidity_icon = Image.open('./lib/oled/humidity_icon.png')  # 16x16 icon for humidity

def display_environmental_data():
    while True:
        # Read BME280 sensor data
        temperature = sensor.read_temperature()
        pressure = sensor.read_pressure() / 100.0  # Convert to hPa
        humidity = sensor.read_humidity()

        # Create a new image for drawing
        image = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Draw titles and icons
        image.paste(temp_icon, (5, 5))
        draw.text((25, 5), f"Temp: {temperature:.1f}C", font=fontSmall, fill="BLUE")

        image.paste(pressure_icon, (5, 25))
        draw.text((25, 25), f"Press: {pressure:.1f}hPa", font=fontSmall, fill="BLUE")

        image.paste(humidity_icon, (5, 45))
        draw.text((25, 45), f"Hum: {humidity:.1f}%", font=fontSmall, fill="BLUE")

        # Display the image
        disp.ShowImage(image, 0, 0)

        # Wait before updating
        time.sleep(2)

if __name__ == "__main__":
    try:
        print("Starting the OLED display program...")
        display_environmental_data()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Clearing display.")
        disp.clear()
