import paho.mqtt.client as mqtt
import pymysql
from datetime import datetime

BROKER = "192.168.0.100"
TOPIC_ENTRY = "parking/entry"
TOPIC_EXIT = "parking/exit"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "parking_db",
}

# Funkcja obsługi wjazdu
def process_entry(rfid_id, entry_time):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO aktualne_wjazdy (rfid_id, data_wjazdu) VALUES (%s, %s)", (rfid_id, entry_time))
    conn.commit()
    conn.close()

# Funkcja obsługi wyjazdu
def process_exit(rfid_id, exit_time):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Pobranie danych wjazdu
    cursor.execute("SELECT data_wjazdu FROM aktualne_wjazdy WHERE rfid_id = %s", (rfid_id,))
    row = cursor.fetchone()
    if row:
        entry_time = row[0]
        # Przeniesienie wpisu do archiwum
        cursor.execute("INSERT INTO archiwum (rfid_id, data_wjazdu, data_wyjazdu) VALUES (%s, %s, %s)",
                       (rfid_id, entry_time, exit_time))
        # Usunięcie wpisu z aktualnych wjazdów
        cursor.execute("DELETE FROM aktualne_wjazdy WHERE rfid_id = %s", (rfid_id,))
        conn.commit()

    conn.close()

# Funkcje MQTT
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == TOPIC_ENTRY:
        rfid_id, entry_time = payload.split(",")
        process_entry(rfid_id, entry_time)
    elif msg.topic == TOPIC_EXIT:
        rfid_id, exit_time = payload.split(",")
        process_exit(rfid_id, exit_time)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER)
client.subscribe([(TOPIC_ENTRY, 0), (TOPIC_EXIT, 0)])
client.loop_forever()
