#!/usr/bin/env python3

import time
import threading
import board
import busio
import neopixel
from config import buttonRed, buttonGreen, ws2812pin
import RPi.GPIO as GPIO
import adafruit_bme280.advanced as adafruit_bme280

# Domyślne zakresy parametrów
temperature_range = [21, 22, 23, 24, 25, 26, 27, 28]
humidity_range = [20, 30, 40, 50, 60, 70, 80, 88]

# Kolory stałe dla diod WS2812 (odwrócona kolejność)
LED_COLORS = [
    (255, 0, 0),  # Dioda 6-8: czerwony
    (255, 0, 0),
    (255, 0, 0),
    (0, 255, 0),  # Dioda 4-5: zielony
    (0, 255, 0),
    (0, 0, 255),  # Dioda 1-3: niebieski
    (0, 0, 255),
    (0, 0, 255),
]

# Inicjalizacja WS2812
pixels = neopixel.NeoPixel(board.D8, 8, brightness=1.0 / 32, auto_write=False)

# Zmienne globalne
current_parameter = 0  # 0: temperatura, 1: wilgotność
last_switch_time = time.time()

# Konfiguracja BME280
def bme280_config():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    return bme280

# Odczyt z BME280
def bme280_read(bme):
    return {"temperature": bme.temperature, "humidity": bme.humidity}

# Konfiguracja diod WS2812
def diode_configuration(pixel, param_value, param_range):
    pixel.fill((0, 0, 0))  # Wyłączenie wszystkich diod
    for i in range(len(param_range) - 1):
        if param_value >= param_range[i] and param_value < param_range[i + 1]:
            # Zapisz odpowiednią liczbę diod zgodnie z przedziałem
            for j in range(i + 1):
                pixel[7 - j] = LED_COLORS[j]  # Odwrócone przypisanie kolorów
            break
    pixel.show()

# Obsługa przycisku czerwonego
def button_red_pressed_callback(channel):
    global current_parameter
    current_parameter = 0
    print("Przełączono na wyświetlanie temperatury.")

# Obsługa przycisku zielonego
def button_green_pressed_callback(channel):
    global current_parameter
    current_parameter = 1
    print("Przełączono na wyświetlanie wilgotności.")

# Funkcja do zmiany zakresów komfortu
def update_comfort_ranges():
    global temperature_range, humidity_range
    while True:
        print("\nObecne zakresy:")
        print(f"Temperatura: {temperature_range}")
        print(f"Wilgotność: {humidity_range}")
        print("Wybierz opcję:")
        print("1: Zmień zakres temperatury")
        print("2: Zmień zakres wilgotności")
        print("3: Wyjdź z edytora")
        choice = input("Wybór: ")

        if choice == "1":
            try:
                new_range = input("Wprowadź nowy zakres temperatury (np. 21,22,23,24,25,26,27,28): ")
                temperature_range = list(map(int, new_range.split(",")))
                print("Zakres temperatury zaktualizowany.")
            except ValueError:
                print("Nieprawidłowy format.")
        elif choice == "2":
            try:
                new_range = input("Wprowadź nowy zakres wilgotności (np. 20,30,40,50,60,70,80,88): ")
                humidity_range = list(map(int, new_range.split(",")))
                print("Zakres wilgotności zaktualizowany.")
            except ValueError:
                print("Nieprawidłowy format.")
        elif choice == "3":
            print("Zakończono edycję zakresów.")
            break
        else:
            print("Nieprawidłowy wybór.")

# Główna funkcja programu
if __name__ == "__main__":
    try:
        # Inicjalizacja BME280
        bme1 = bme280_config()

        # Konfiguracja przycisków
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=button_red_pressed_callback, bouncetime=200)
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=button_green_pressed_callback, bouncetime=200)

        # Wątek dla edytora zakresów
        threading.Thread(target=update_comfort_ranges, daemon=True).start()

        # Pętla główna
        while True:
            parameters = bme280_read(bme1)
            if current_parameter == 0:  # Wyświetlanie temperatury
                diode_configuration(pixels, parameters["temperature"], temperature_range)
            elif current_parameter == 1:  # Wyświetlanie wilgotności
                diode_configuration(pixels, parameters["humidity"], humidity_range)

            # Automatyczne przełączanie co 10 sekund
            if time.time() - last_switch_time > 10:
                current_parameter = (current_parameter + 1) % 2
                last_switch_time = time.time()

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program przerwany. Czyszczenie GPIO...")
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        GPIO.cleanup()
