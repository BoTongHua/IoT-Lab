#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from config import *
from mfrc522 import MFRC522
import paho.mqtt.client as mqtt

broker = "localhost"
topic = "rfid/usage"
client = mqtt.Client()

def buzzer_and_led_feedback():
    # Turn on the buzzer and LED
    buzzer(True)
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=0.1, auto_write=False)
    pixels.fill((0, 255, 0))  # Green for successful scan
    pixels.show()
    time.sleep(0.5)
    # Turn off the buzzer and LED
    buzzer(False)
    pixels.fill((0, 0, 0))
    pixels.show()

def rfid_read():
    MIFAREReader = MFRC522()
    last_uid = None

    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                uid_string = ".".join(str(x) for x in uid)
                if uid_string != last_uid:  # Check if it's a new card
                    last_uid = uid_string
                    current_time = time.ctime()
                    print(f"Card read UID: {uid_string} at {current_time}")
                    
                    # MQTT publish
                    client.publish(topic, f"{uid_string},{current_time}")
                    
                    # Feedback
                    buzzer_and_led_feedback()
                time.sleep(1)  # Delay to avoid rapid re-reads

def connect_mqtt():
    client.connect(broker)
    client.loop_start()

def run_rfid_publisher():
    connect_mqtt()
    try:
        rfid_read()
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_rfid_publisher()
