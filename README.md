# ESP_LCD MicroPython driver for the TTGO T-Display-S3 st7789 display

Warning: This is a work in progress and may contain bugs and/or incorrect documentation.

This driver is based on [devbis' st7789_mpy driver.](https://github.com/devbis/st7789_mpy)
I modified the original driver for one of my projects to add:

- Support for the TTGO T-Dispay-S3 with a parallel interface using the ESP_LCD
  interface with DMA.
- Display framebuffer enabling alpha blending for many drawing methods.
- Display Rotation.
- Scrolling
- Writing text using bitmaps converted from True Type fonts
- Drawing text using 8 and 16-bit wide bitmap fonts
- Drawing text using Hershey vector fonts
- Drawing JPGs using the TJpgDec - Tiny JPEG Decompressor R0.01d. from
  http://elm-chan.org/fsw/tjpgd/00index.html
- Drawing PNGs using the pngle library from https://github.com/kikuchan/pngle
- Drawing and rotating Polygons and filled Polygons

Included are 12 bitmap fonts derived from classic pc text mode fonts, 26
Hershey vector fonts and several example programs for different devices.


## Pre-compiled firmware

The firmware directory contains pre-compiled MicroPython v1.20.0 firmware compiled
using ESP IDF v4.4.4 The firmware includes the st7789 C driver and several frozen
python font files. See the README.md file in the fonts folder for more information
about the font files.


## Thanks go out to:

- https://github.com/devbis for the original driver this is based on.
- https://github.com/hklang10 for letting me know of the new mp_raise_ValueError().
- https://github.com/aleggon for finding the correct offsets for 240x240
  displays and for discovering issues compiling STM32 ports.

-- Russ

## Overview

This is a driver for MicroPython to handle cheap displays based on the ST7789
chip. The driver is written in C.

<p align="center">
  <img src="https://raw.githubusercontent.com/russhughes/st7789_mpy/master/docs/ST7789.jpg" alt="ST7789 display photo"/>
</p>


# Setup MicroPython Build Environment in Ubuntu 20.04.2

See the MicroPython
[README.md](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md#setting-up-esp-idf-and-the-build-environment)
if you run into any build issues not directly related to the st7789 driver. The
recommended MicroPython build instructions may have changed.

Update and upgrade Ubuntu using apt-get if you are using a new install of
Ubuntu or the Windows Subsystem for Linux.

```bash
sudo apt-get -y update
sudo apt-get -y upgrade
```

Use apt-get to install the required build tools.

```bash
sudo apt-get -y install build-essential libffi-dev git pkg-config cmake virtualenv python3-pip python3-virtualenv
```

### Install a compatible esp-idf SDK

The MicroPython README.md states: "The ESP-IDF changes quickly, and MicroPython
only supports certain versions. I have had good luck using IDF v4.4.3

Clone the esp-idf SDK repo -- this usually takes several minutes.

```bash
git clone -b v4.4.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf/
git pull
```

If you already have a copy of the IDF, you can checkout a version compatible
with MicroPython and update the submodules using:

```bash
$ cd esp-idf
$ git checkout v4.4.3
$ git submodule update --init --recursive
```

Install the esp-idf SDK.

```bash
./install.sh
```

Source the esp-idf export.sh script to set the required environment variables.
You must source the file and not run it using ./export.sh. You will need to
source this file before compiling MicroPython.

```bash
source export.sh
cd ..
```

Clone the MicroPython repo.

```bash
git clone https://github.com/micropython/micropython.git
```

Clone the st7789 driver repo.

```bash
git clone https://github.com/russhughes/st7789s3_mpy.git
```

Update the git submodules and compile the MicroPython cross-compiler

```bash
cd micropython/
git submodule update --init
cd mpy-cross/
make
cd ..
cd ports/esp32
```

Copy any .py files you want to include in the firmware as frozen python modules
to the modules subdirectory in ports/esp32. Be aware there is a limit to the
flash space available. You will know you have exceeded this limit if you
receive an error message saying the code won't fit in the partition or if your
firmware continuously reboots with an error.

For example:

```bash
cp ../../../st7789s3_mpy/fonts/bitmap/vga1_16x16.py modules
cp ../../../st7789s3_mpy/fonts/truetype/NotoSans_32.py modules
cp ../../../st7789s3_mpy/fonts/vector/scripts.py modules
```

Build the MicroPython firmware with the driver and frozen .py files in the
modules directory. If you did not add any .py files to the modules directory,
you can leave out the FROZEN_MANIFEST and FROZEN_MPY_DIR settings.

```bash
make USER_C_MODULES=../../../../st7789s3_mpy/st7789/micropython.cmake FROZEN_MANIFEST="" FROZEN_MPY_DIR=$UPYDIR/modules
```

Erase and flash the firmware to your device. Set PORT= to the ESP32's usb
serial port. I could not get the USB serial port to work under the Windows
Subsystem (WSL2) for Linux. If you have the same issue, you can copy the
firmware.bin file and use the Windows esptool.py to flash your device.

```bash
make USER_C_MODULES=../../../../st7789s3_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 erase
make USER_C_MODULES=../../../../st7789s3_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 deploy
```

The firmware.bin file will be in the build-GENERIC directory. To flash using
the python esptool.py utility. Use pip3 to install the esptool if it's not
already installed.

```bash
pip3 install esptool
```

Set PORT= to the ESP32's USB serial port

```bash
esptool.py --port COM3 erase_flash
esptool.py --chip esp32 --port COM3 write_flash -z 0x0 firmware.bin
```
## CMake building instructions for MicroPython 1.14 and later

for ESP32:

    $ cd micropython/ports/esp32

And then compile the module with specified USER_C_MODULES dir.

    $ make USER_C_MODULES=../../../../st7789s3_mpy/st7789/micropython.cmake


## Methods

Note: Optional Parameters are shown enclosed in '{' and '}' characters.

- `st7789.ST7789(width, height, d7, d6, d5, d4, d3, d2, d1, d0, wr, rd, reset, dc, cs {, backlight, power, rotations, rotation, color_order, inversion, options})`

    ### Required positional arguments:
    - `width` display width
    - `height` display height
    - `d7`: 8-bit data bus pin bit 7 (Most significant bit)
    - `d6`: 8-bit data bus pin bit 6
    - `d5`: 8-bit data bus pin bit 5
    - `d4`: 8-bit data bus pin bit 4
    - `d3`: 8-bit data bus pin bit 3
    - `d2`: 8-bit data bus pin bit 2
    - `d1`: 8-bit data bus pin bit 1
    - `d0`: 8-bit data bus pin bit 0 (Least significant bit)
    - `wr`: write strobe pin
    - `rd`: read strobe pin
    - `reset` sets the pin connected to the display's hardware reset
    - `dc` sets the pin connected to the display data/command selection input.
    - `cs` sets the pin connected to the displays chip select input.

    ### Optional keyworld arguments:

    - `backlight` sets the pin connected to the display's backlight enable
      input. The display's backlight input can often be left floating or
      disconnected as the backlight on some displays is always powered on and
      cannot be turned off.

    - `power` sets the pin connected to the display's power enable input.

    - `rotations` sets the orientation table. The orientation table is a list
      of tuples for each `rotation` used to set the width, height, x_gap,
      y_gap, swap_xy, mirror_x, and mirror_y values.

      Default `rotations` are included for the following st7789 and st7735
      display sizes:

      Display | Default Orientation Tables
      ------- | --------------------------
      240x320 | [(240, 320, 0, 0, false, false, false), (320, 240, 0, 0, true, true, false), (240, 320, 0, 0, false, true, true), (320, 240, 0, 0, true, false, true)]
      170x320 | [(170, 320, 35, 0, false, false, false), (320, 170, 0, 35, true, true, false), (170, 320, 35, 0, false, true, true), (320, 170, 0, 35, true, false, true)]
      240x240 | [(240, 240, 0, 0, false, false, false), (240, 240, 0, 0, true, true, false), (240, 240, 0, 80, false, true, true), (240, 240, 80, 0, true, false, true)]
      135x240 | [(135, 240, 52, 40, false, false, false), (240, 135, 40, 53, true, true, false), (135, 240, 53, 40, false, true, true), (240, 135, 40, 52, true, false, true)]
      128x160 | [(128, 160, 0, 0, false, false, false), (160, 128, 0, 0, true, true, false), (128, 160, 0, 0, false, true, true), (160, 128, 0, 0, true, false, true)]
      128x128 | [(128, 128, 2, 1, false, false, false), (128, 128, 1, 2, true, true, false), (128, 128, 2, 3, false, true, true), {128, 128, 3, 2, true, false, true)]

      You may define up to 4 rotations.

    - `rotation` sets the display rotation according to the orientation table.

      The default orientation table defines four counter-clockwise rotations
      for 240x320, 240x240, 134x240, 128x160 and 128x128 displays with the
      LCD's ribbon cable at the bottom of the display. The default rotation is
      Portrait (0 degrees).

      Index | Rotation
      ----- | --------
      0     | Portrait (0 degrees)
      1     | Landscape (90 degrees)
      2     | Reverse Portrait (180 degrees)
      3     | Reverse Landscape (270 degrees)

    - `color_order` sets the color order used by the driver (st7789.RGB or
      st7789.BGR)

    - `inversion` Sets the display color inversion mode if True, clears the
      display color inversion mode if false.

    - `options` Sets driver option flags.

      Option        | Description
      ------------- | -----------
      st7789.WRAP   | pixels, lines, polygons, and Hershey text will wrap around the display both horizontally and vertically.
      st7789.WRAP_H | pixels, lines, polygons, and Hershey text will wrap around the display horizontally.
      st7789.WRAP_V | pixels, lines, polygons, and Hershey text will wrap around the display vertically.

- `deinit()`

    Frees memory used by buffers and deletes the dedicated GPIO bundle.  This
    method should be called before reinitalizing the display without hard
    resetting the microcontroller.

- `show({wait})`

    Update the display from the framebuffer. If the optional `wait` parameter is
    True, this method blocks until the display refresh is complete.  You must
    use show() method to update the display before you will see anything on the
    display.

- `inversion_mode(bool)` Sets the display color inversion mode if True, clears
  the display color inversion mode if False.

- `init()`

  Must be called to initialize the display.

- `on()`

  Turn on the backlight pin if one was defined during init.

- `off()`

  Turn off the backlight pin if one was defined during init.

- `fill({color, alpha})`

  Fill the display with the specified color optionally `alpha` blended with the
  background. `color` defaults to BLACK, `alpha` defaults to 255.

- `pixel(x, y {, color, alpha})`

  Set the specified pixel to the given `color`. `color` defaults to WHITE,
  `alpha` defaults to 255.

- `line(x0, y0, x1, y1 {, color, aplha})`

  Draws a single line with the provided `color` from (`x0`, `y0`) to (`x1`,
  `y1`). `color` defaults to BLACK, `alpha` defaults to 255.

- `hline(x, y, w {, color, alpha})`

  Draws a single horizontal line with the provided `color` and `length` in
  pixels. `color` defaults to BLACK, `alpha` defaults to 255.

- `vline(x, y, length {, color, alpha})`

  Draws a single horizontal line with the provided `color` and `length` in
  pixels. `color` defaults to BLACK, `alpha` defaults to 255.

- `rect(x, y, width, height {, color, alpha})`

  Draws a rectangle from (`x`, `y`) with corresponding dimensions. `color`
  defaults to BLACK, `alpha` defaults to 255.

- `fill_rect(x, y, width, height {, color, alpha})`

  Fill rectangle `width` by `height` starting at `x`, `y` with `color`
  optionally `alpha` blended with the background. `color` defaults to BLACK,
  `alpha` defaults to 255.

- `circle(x, y, r {, color, alpha})`

  Draws a circle with radius `r` centered at the (`x`, `y`) coordinates in the
  given `color`. `color` defaults to BLACK,
  `alpha` defaults to 255.

- `fill_circle(x, y, r {, color, alpha})`

  Draws a filled circle with radius `r` centered at the (`x`, `y`) coordinates
  in the given `color`. `color` defaults to BLACK, `alpha` defaults to 255.

- `blit_buffer(buffer, x, y, width, height {, alpha})`

  Copy bytes() or bytearray() content to the screen internal memory. Note:
  every color requires 2 bytes in the array. `alpha` defaults to 255.

- `text(font, s, x, y {, fg, bg, alpha})`

  Write text to the display using the specified bitmap `font` with the
  coordinates as the upper-left corner of the text. The optional arguments `fg`
  and `bg` can set the foreground and background colors of the text; otherwise
  the foreground color defaults to `WHITE`, and the background color defaults
  to `BLACK`. `alpha` defaults to 255. See the `README.md` in the
  `fonts/bitmap` directory for example fonts.

- `write(bitmap_font, s, x, y {, fg, bg, alpha})`

  Write text to the display using the specified proportional or Monospace
  bitmap font module with the coordinates as the upper-left corner of the text.
  The foreground and background colors of the text can be set by the optional
  arguments `fg` and `bg`, otherwise the foreground color defaults to `WHITE`
  and the background color defaults to `BLACK`. `alpha` defaults to 255.

  See the `README.md` in the `truetype/fonts` directory for example fonts.
  Returns the width of the string as printed in pixels. Accepts UTF8 encoded
  strings.

  The `font2bitmap` utility creates compatible 1 bit per pixel bitmap modules
  from Proportional or Monospaced True Type fonts. The character size,
  foreground, background colors, and characters in the bitmap module may be
  specified as parameters. Use the -h option for details. If you specify a
  buffer_size during the display initialization, it must be large enough to
  hold the widest character (HEIGHT * MAX_WIDTH * 2).

- `write_len(bitap_font, s)`

  Returns the string's width in pixels if printed in the specified font.

- `draw(vector_font, s, x, y {, fg, scale, alpha})`

  Draw text to the display using the specified Hershey vector font with the
  coordinates as the lower-left corner of the text. The foreground color of the
  text can be set by the optional argument `fg`. Otherwise the foreground color
  defaults to `WHITE`. The size of the text can be scaled by specifying a
  `scale` value. The `scale` value must be larger than 0 and can be a
  floating-point or an integer value. The `scale` value defaults to 1.0.
  `alpha` defaults to 255. See the README.md in the `vector/fonts` directory,
  for example fonts and the utils directory for a font conversion program.

- `draw_len(vector_font, s {, scale})`

  Returns the string's width in pixels if drawn with the specified font.

- `jpg(jpg_filename, x, y)`

  Draw a JPG file on the display at the given `x` and `y` coordinates as the
  upper left corner of the image. This method requires an additional 3100 bytes
  of memory for it's work buffer.

- `jpg_decode(jpg_filename {, x, y, width, height})`

  Decode a jpg file and return it or a portion of it as a tuple composed of
  (buffer, width, height). The buffer is a color565 blit_buffer compatible byte
  array. The buffer will require width * height * 2 bytes of memory.

  If the optional x, y, width, and height parameters are given, the buffer will
  only contain the specified area of the image. See
  examples/T-DISPLAY/clock/clock.py and
  examples/T-DISPLAY/toasters_jpg/toasters_jpg.py for examples.

- `png(png_filename, x, y)`

  Draw a PNG file on the display with upper left corner of the image at the
  given `x` and `y` coordinates. The PNG will not be clipped it must be able to
  fit fully on the display or it will not be drawn. Transparency is supported,
  see the alien.py program in the examples/png folder for an example.

- `polygon_center(polygon)`

   Return the center of the `polygon` as an (x, y) tuple. The `polygon` should
   consist of a list of (x, y) tuples forming a closed convex polygon.

- `fill_polygon(polygon, x, y, color {, alpha, angle, center_x, center_y})`

  Draw a filled `polygon` at the `x`, and `y` coordinates in the `color` given.
  `alpha` defaults to 255. The polygon may be rotated `angle` radians about the
  `center_x` and `center_y` point. The polygon should consist of a list of (x,
  y) tuples forming a closed convex polygon.

  See the TWATCH-2020 `watch.py` demo for an example.

- `polygon(polygon, x, y, color {, alpha, angle, center_x, center_y)`

  Draw a `polygon` at the `x`, and `y` coordinates in the `color` given.
  `alpha` defaults to 255. The polygon may be rotated `angle` radians about the
  `center_x` and `center_y` point. The polygon should consist of a list of (x,
  y) tuples forming a closed convex polygon.

  See the T-Display `roids.py` for an example.

- `bitmap(bitmap, x , y {, alpha, index})` or `bitmap((bitmap_as_bytes, w, h), x , y {, alpha})`

  Draw a bitmap using the specified `x`, `y` coordinates as the upper-left
  corner of the `bitmap`.

  - If the `bitmap` parameter is a bitmap module, the `index` parameter may be
    specified to select a specific bitmap from the module. The `index`
    parameter must be an integer value greater than or equal to 0 and less than
    the number of bitmaps in the module. The `index` value defaults to 0.
    `alpha` defaults to 255.

  - If the `bitmap_module` parameter is a tuple, the tuple must contain a
    bitmap as a byte array, the width of the bitmap in pixels, and the height
    of the bitmap in pixels. `alpha` defaults to 255.

  The `imgtobitmap.py` utility creates compatible 1 to 8 bit per pixel bitmap
  modules from image files using the Pillow Python Imaging Library.

  The `monofont2bitmap.py` utility creates compatible 1 to 8 bit per pixel
  bitmap modules from Monospaced True Type fonts. See the `inconsolata_16.py`,
  `inconsolata_32.py` and `inconsolata_64.py` files in the `examples/lib`
  folder for sample modules and the `mono_font.py` program for an example using
  the generated modules.

  The character sizes, bit per pixel, foreground, background colors, and the
  characters to include in the bitmap module may be specified as parameters.
  Use the -h option for details. Bits per pixel settings larger than one may be
  used to create antialiased characters at the expense of memory use.

- `width()`

  Returns the current logical width of the display. (ie a 135x240 display
  rotated 90 degrees is 240 pixels wide)

- `height()`

  Returns the current logical height of the display. (ie a 135x240 display
  rotated 90 degrees is 135 pixels high)

- `rotation(r)`

  Set the rotates the logical display in a counter-clockwise direction.
  0-Portrait (0 degrees), 1-Landscape (90 degrees), 2-Inverse Portrait (180
  degrees), 3-Inverse Landscape (270 degrees)

The module exposes predefined colors:
  `BLACK`, `BLUE`, `RED`, `GREEN`, `CYAN`, `MAGENTA`, `YELLOW`, and `WHITE`

## Scrolling

The st7789 display controller contains a 240 by 320-pixel frame buffer used to
store the pixels for the display. For scrolling, the frame buffer consists of
three separate areas; The (`tfa`) top fixed area, the (`height`) scrolling
area, and the (`bfa`) bottom fixed area. The `tfa` is the upper portion of the
frame buffer in pixels not to scroll. The `height` is the center portion of the
frame buffer in pixels to scroll. The `bfa` is the lower portion of the frame
buffer in pixels not to scroll. These values control the ability to scroll the
entire or a part of the display.

For displays that are 320 pixels high, setting the `tfa` to 0, `height` to 320,
and `bfa` to 0 will allow scrolling of the entire display. You can set the
`tfa` and `bfa` to a non-zero value to scroll a portion of the display. `tfa` +
`height` + `bfa` = should equal 320, otherwise the scrolling mode is undefined.

Displays less than 320 pixels high, the `tfa`, `height`, and `bfa` will need to
be adjusted to compensate for the smaller LCD panel. The actual values will
vary depending on the configuration of the LCD panel. For example, scrolling
the entire 135x240 TTGO T-Display requires a `tfa` value of 40, `height` value
of 240, and `bfa` value of 40 (40+240+40=320) because the T-Display LCD shows
240 rows starting at the 40th row of the frame buffer, leaving the last 40 rows
of the frame buffer undisplayed.

Other displays like the Waveshare Pico LCD 1.3 inch 240x240 display require the
`tfa` set to 0, `height` set to 240, and `bfa` set to 80 (0+240+80=320) to
scroll the entire display. The Pico LCD 1.3 shows 240 rows starting at the 0th
row of the frame buffer, leaving the last 80 rows of the frame buffer
undisplayed.

The `vscsad` method sets the (VSSA) Vertical Scroll Start Address. The VSSA
sets the line in the frame buffer that will be the first line after the `tfa`.

    The ST7789 datasheet warns:

    The value of the vertical scrolling start address is absolute (with reference to the frame memory),
    it must not enter the fixed area (defined by Vertical Scrolling Definition, otherwise undesirable
    image will be displayed on the panel.

- `vscrdef(tfa, height, bfa)` Set the vertical scrolling parameters.

  `tfa` is the top fixed area in pixels. The top fixed area is the upper
  portion of the display frame buffer that will not be scrolled.

  `height` is the total height in pixels of the area scrolled.

  `bfa` is the bottom fixed area in pixels. The bottom fixed area is the lower
  portion of the display frame buffer that will not be scrolled.

- `vscsad(vssa)` Set the vertical scroll address.

  `vssa` is the vertical scroll start address in pixels. The vertical scroll
  start address is the line in the frame buffer will be the first line shown
  after the TFA.

## Helper functions

- `color565(r, g, b)`

  Pack a color into 2-bytes rgb565 format

- `map_bitarray_to_rgb565(bitarray, buffer, width {, color, bg_color})`

  Convert a `bitarray` to the rgb565 color `buffer` suitable for blitting. Bit
  1 in `bitarray` is a pixel with `color` and 0 - with `bg_color`.
