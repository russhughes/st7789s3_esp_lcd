"""
hello.py

    Writes "Hello!" in random colors at random locations on the display.
"""

import random
import time
import st7789
import tft_config
import vga1_bold_16x32 as font

tft = tft_config.config(0)

def color_wheel(position):
    """returns a 565 color from the given position of the color wheel"""
    position = (255 - position) % 255

    if position < 85:
        return st7789.color565(255 - position * 3, 0, position * 3)

    if position < 170:
        position -= 85
        return st7789.color565(0, position * 3, 255 - position * 3)

    position -= 170
    return st7789.color565(position * 3, 255 - position * 3, 0)


def center(text):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        st7789.RED)

def main():
    try:
        tft.init()
        tft.fill(st7789.RED)
        center("Hello!")
        tft.show()
        time.sleep(2)

        wheel = 0

        while True:
            for rotation in range(4):
                tft.rotation(rotation)
                tft.fill(st7789.BLACK)

                col_max = tft.width() - font.WIDTH*6
                row_max = tft.height() - font.HEIGHT

                for i in range(10):
                    wheel = (wheel + 1) % 255
                    opacity = (i * 255 // 10)

                    tft.text(
                        font,
                        "Hello!",
                        random.randint(0, col_max),
                        random.randint(0, row_max),
                        color_wheel(wheel),
                        st7789.TRANSPARENT,
                        opacity)

                    tft.show()
                    time.sleep(0.05)
    finally:
        tft.deinit()

main()
