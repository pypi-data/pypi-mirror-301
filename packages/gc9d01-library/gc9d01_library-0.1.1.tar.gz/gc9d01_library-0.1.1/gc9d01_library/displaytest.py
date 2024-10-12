from GC9D01 import GC9D01
import board
import busio
import digitalio
import time

# Setup SPI communication
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
spi.try_lock()
spi.configure(baudrate=24000000, phase=0, polarity=0)
spi.unlock()

# Setup control pins
cs = digitalio.DigitalInOut(board.CE0)  # Chip Select
dc = digitalio.DigitalInOut(board.D25)  # Data/Command
rst = digitalio.DigitalInOut(board.D24)  # Reset

# Create display object
display = GC9D01(spi, dc, cs, rst)
time.sleep(0.1)  # Short delay after initialization

# Test function to cycle through different colors
def color_test(display):
    # Define a list of colors in 16-bit RGB565 format
    colors = [
        0xF800,  # Red
        0x07E0,  # Green
        0x001F,  # Blue
        0xFFE0,  # Yellow
        0xF81F,  # Magenta
        0x07FF,  # Cyan
        0xFFFF,  # White
        0x0000   # Black
    ]
    
    # Cycle through each color
    for color in colors:
        display.fill_screen(color)
        time.sleep(1)  # Wait for 1 second before next color

# Run the color test
color_test(display)
