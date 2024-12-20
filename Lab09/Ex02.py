#!/usr/bin/env python3

import time
import board
import busio
import neopixel
from config import buttonRed, buttonGreen, ws2812pin
import RPi.GPIO as GPIO
import adafruit_bme280.advanced as adafruit_bme280

# Zakresy parametrów
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

# Główna funkcja programu
if __name__ == "__main__":
    try:
        # Inicjalizacja BME280
        bme1 = bme280_config()

        # Konfiguracja przycisków
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=button_red_pressed_callback, bouncetime=200)
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=button_green_pressed_callback, bouncetime=200)

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
