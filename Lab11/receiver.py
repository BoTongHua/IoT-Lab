#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sqlite3
import time
import tkinter as tk

broker = "localhost"
topic = "rfid/usage"
client = mqtt.Client()

def save_to_database(uid, timestamp):
    connection = sqlite3.connect("workers.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO workers_log VALUES (?, ?, ?)", (timestamp, uid, "RFID Reader"))
    connection.commit()
    connection.close()

def process_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    uid, timestamp = payload.split(",")
    print(f"Received UID: {uid} at {timestamp}")
    save_to_database(uid, timestamp)

def run_gui():
    window = tk.Tk()
    window.title("RFID Logs")
    window.geometry("300x200")

    def display_logs():
        connection = sqlite3.connect("workers.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM workers_log")
        logs = cursor.fetchall()
        log_window = tk.Toplevel()
        for log in logs:
            tk.Label(log_window, text=f"{log[0]} - UID: {log[1]}").pack()
        connection.close()

    tk.Button(window, text="Show Logs", command=display_logs).pack()
    tk.Button(window, text="Exit", command=window.quit).pack()
    window.mainloop()

def connect_mqtt():
    client.on_message = process_message
    client.connect(broker)
    client.subscribe(topic)
    client.loop_start()

def run_receiver():
    connect_mqtt()
    run_gui()
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    run_receiver()
