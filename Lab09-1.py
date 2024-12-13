import RPi.GPIO as GPIO
import time
from config import led1, encoderLeft, encoderRight

# PWM frequency
PWM_FREQUENCY = 1000

# Initial brightness level (0-100%)
brightness = 50

# Setup PWM on LED 1
GPIO.setup(led1, GPIO.OUT)
pwm_led1 = GPIO.PWM(led1, PWM_FREQUENCY)
pwm_led1.start(brightness)

# Encoder callback functions
def increase_brightness(channel):
    global brightness
    if brightness < 100:
        brightness += 5
        pwm_led1.ChangeDutyCycle(brightness)
        print(f"Brightness increased to {brightness}%")

def decrease_brightness(channel):
    global brightness
    if brightness > 0:
        brightness -= 5
        pwm_led1.ChangeDutyCycle(brightness)
        print(f"Brightness decreased to {brightness}%")

# Setup event detection for the rotary encoder
GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=decrease_brightness, bouncetime=200)
GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=increase_brightness, bouncetime=200)

try:
    print("Adjust LED brightness using the rotary encoder.")
    print("Press Ctrl+C to exit.")
    while True:
        time.sleep(0.1)  # Keep the script running

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    pwm_led1.stop()
    GPIO.cleanup()
