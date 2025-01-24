import time
from datetime import datetime
import paho.mqtt.client as mqtt
from mfrc522 import MFRC522
import RPi.GPIO as GPIO

BROKER = "192.168.0.100"
TOPIC_EXIT = "parking/exit"

# GPIO i RFID
GPIO.setmode(GPIO.BOARD)
reader = MFRC522()

# Funkcja odczytu RFID
def read_rfid():
    while True:
        (status, _) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == reader.MI_OK:
            (status, uid) = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                card_id = "".join([str(x) for x in uid])
                return card_id

# Funkcja obsługi wyjazdu
def handle_exit(client, card_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client.publish(TOPIC_EXIT, f"{card_id},{now}")

# Połączenie MQTT
def on_connect(client, userdata, flags, rc):
    print("Połączono z MQTT brokerem.")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER)

if __name__ == "__main__":
    client.loop_start()
    try:
        while True:
            card_id = read_rfid()
            handle_exit(client, card_id)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.loop_stop()
