import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

led_pins = [
    board.IO21,
    board.IO26, # type: ignore
    board.IO47,
    board.IO33, # type: ignore
    board.IO34, # type: ignore
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39
]

leds = [DigitalInOut(pin) for pin in led_pins]

for led in leds:
    led.direction = Direction.OUTPUT

# Initializing variables
filtered_volume = 0
alpha_rise = 0.8
alpha_fall = 0.1
min_volume = microphone.value  # Initialize 0 value
max_volume = 50000   # Max expected volume

# main loop
while True:
    volume = microphone.value

    # Apply exponential filter:
    # Quickly rise when volume increases
    # Slowly fall when volume decreases
    if volume > filtered_volume:
        filtered_volume = alpha_rise * volume + (1 - alpha_rise) * filtered_volume
    else:
        filtered_volume = alpha_fall * volume + (1 - alpha_fall) * filtered_volume

    print(f"Raw Volume: {volume}, Filtered Volume: {filtered_volume}")

    # Control the LEDs based on the filtered volume
    for i in range(11):
        threshold = (i + 1) * max_volume / 11
        if filtered_volume > threshold:
            leds[i].value = 1
        else:
            leds[i].value = 0

    sleep(0.1)
