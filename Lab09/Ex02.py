from config import *
import w1thermsensor
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import neopixel
import time

# WS2812 configuration
NUM_PIXELS = 8  # Number of LEDs in the strip
pixels = neopixel.NeoPixel(ws2812pin, NUM_PIXELS, brightness=0.5, auto_write=True)

# Sensor setup
def read_ds18b20():
    sensor = w1thermsensor.W1ThermSensor()
    return sensor.get_temperature()

def read_bme280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    return bme280.temperature, bme280.humidity, bme280.pressure

# Visualize parameters using WS2812 LEDs
def visualize_parameters(temp, humidity, pressure):
    temp_color = (int(temp * 2.55), 0, 0)  # Red proportional to temperature
    humidity_color = (0, int(humidity * 2.55), 0)  # Green proportional to humidity
    pressure_color = (0, 0, int((pressure - 900) * 255 / 200))  # Blue proportional to pressure range

    for i in range(NUM_PIXELS):
        if i < NUM_PIXELS // 3:
            pixels[i] = temp_color
        elif i < 2 * NUM_PIXELS // 3:
            pixels[i] = humidity_color
        else:
            pixels[i] = pressure_color

    pixels.show()

# Main program loop
def main():
    print("Starting environment monitoring with WS2812 visualization.")
    try:
        while True:
            ds_temp = read_ds18b20()
            bme_temp, bme_humidity, bme_pressure = read_bme280()

            print(f"DS18B20 Temperature: {ds_temp:.2f} °C")
            print(f"BME280 Temperature: {bme_temp:.2f} °C")
            print(f"BME280 Humidity: {bme_humidity:.2f} %")
            print(f"BME280 Pressure: {bme_pressure:.2f} hPa")

            visualize_parameters(bme_temp, bme_humidity, bme_pressure)
            time.sleep(5)  # Refresh every 5 seconds

    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
