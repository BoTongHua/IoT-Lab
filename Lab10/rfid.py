#!/usr/bin/env python3

# pylint: disable=no-member

import time
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from rpi_ws281x import PixelStrip, Color
from config import buzzerPin, ws2812pin

# LED strip configuration
LED_COUNT = 8  # Number of LED pixels.
LED_PIN = ws2812pin  # GPIO pin connected to the pixels.
LED_BRIGHTNESS = 255  # Brightness of LEDs (0 to 255).

# Initialize LED strip
strip = PixelStrip(LED_COUNT, LED_PIN)
strip.begin()

# Initialize RFID reader
MIFAREReader = MFRC522()

# Keep track of registered cards
registered_cards = {}

# Sound buzzer
def sound_buzzer(duration=0.2):
    GPIO.output(buzzerPin, 0)
    time.sleep(duration)
    GPIO.output(buzzerPin, 1)

# Light up LED strip
def light_up_leds(color, duration=1):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(duration)
    strip.clear()
    strip.show()

def register_card():
    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                # Calculate a unique ID from the UID
                card_id = sum([uid[i] << (i * 8) for i in range(len(uid))])
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Check if the card is already registered
                if card_id not in registered_cards or \
                        (time.time() - registered_cards[card_id]) > 2:  # 2-second timeout
                    registered_cards[card_id] = time.time()
                    print(f"Card {card_id} registered at {current_time}")
                    
                    # Log the card and timestamp
                    with open("card_log.txt", "a") as log_file:
                        log_file.write(f"Card {card_id} registered at {current_time}\n")
                    
                    # Trigger feedback
                    sound_buzzer()
                    light_up_leds(Color(0, 255, 0))  # Green LEDs

                time.sleep(0.5)

if __name__ == "__main__":
    try:
        print("Starting RFID registration program...")
        register_card()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up...")
        strip.clear()
        strip.show()
        GPIO.cleanup()
