# GC9D01 Display Driver for Raspberry Pi

This project provides a Python driver for the GC9D01 round LCD display, designed to work with Raspberry Pi. It includes a library file (`GC9D01.py`) and a test script (`displaytest.py`) to demonstrate basic functionality.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- GC9D01 round LCD display
- Appropriate connections between the Raspberry Pi and the display

## Software Requirements

- Python 3
- CircuitPython libraries (`adafruit_blinka`, `adafruit_circuitpython_busdevice`)

## Installation

1. Clone this repository or download the `gc9d01_library` folder.

2. Install the required libraries:

   ```
   pip3 install adafruit-blinka adafruit-circuitpython-busdevice
   ```

## Wiring

Connect your GC9D01 display to the Raspberry Pi as follows:

| GC9D01 Pin | Raspberry Pi Pin | GPIO Number | Description |
|------------|------------------|-------------|-------------|
| VCC        | Pin 17           | 3.3V        | Power       |
| GND        | Pin 20           | GND         | Ground      |
| SCL        | Pin 23           | GPIO 11     | SPI0 SCLK   |
| SDA        | Pin 19           | GPIO 10     | SPI0 MOSI   |
| CS         | Pin 24           | GPIO 8      | SPI0 CE0    |
| DC         | Pin 22           | GPIO 25     | Data/Command|
| RST        | Pin 18           | GPIO 24     | Reset       |

Note: 
- The pin numbers refer to the physical pin numbers on the Raspberry Pi GPIO header.
- You can change the pin assignments in the `displaytest.py` file if needed, but make sure to update your wiring accordingly.
- Ensure that your Raspberry Pi is powered off when connecting or disconnecting the display to avoid potential damage.

## Usage

1. Import the GC9D01 module in your Python script:

   ```python
   import gc9d01_library
   ```

   Alternatively, you can import the GC9D01 class directly:

   ```python
   from gc9d01_library import GC9D01
   ```

2. Set up the SPI and control pins:

   ```python
   import board
   import busio
   import digitalio

   spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
   cs = digitalio.DigitalInOut(board.CE0)
   dc = digitalio.DigitalInOut(board.D25)
   rst = digitalio.DigitalInOut(board.D24)
   ```

3. Create a display object:

   ```python
   display = gc9d01_library.GC9D01(spi, dc, cs, rst)
   ```

   Or, if you imported the class directly:

   ```python
   display = GC9D01(spi, dc, cs, rst)
   ```

4. Use the display methods to draw on the screen:

   ```python
   display.fill_screen(0xFFFF)  # Fill screen with white
   display.draw_pixel(80, 80, 0xF800)  # Draw a red pixel at (80, 80)
   ```

## Running the Test Script

To run the provided test script:

1. Ensure your display is correctly connected to the Raspberry Pi.
2. Run the following command in the terminal:

   ```
   python3 displaytest.py
   ```

This will cycle through different colors on the display.

## Available Methods

- `fill_screen(color)`: Fill the entire screen with a single color
- `draw_pixel(x, y, color)`: Draw a single pixel at the specified position
- `display_image(image_data)`: Display a full-screen image

Colors are represented in 16-bit RGB565 format.

## Package Structure

The library is structured as follows:

```
gc9d01_library/
    __init__.py
    GC9D01.py
    displaytest.py
```

The `__init__.py` file allows the library to be imported as a Python package.

## Troubleshooting

- If the display doesn't work, double-check your wiring connections.
- Ensure that SPI is enabled on your Raspberry Pi (`raspi-config` > Interface Options > SPI).
- Check that you have the latest version of the required libraries installed.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is open source and available under the [MIT License](LICENSE).