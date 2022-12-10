"""
jpg.py

    Draw a full screen jpg then extract the center 128x128 portion of the jpg using the
    jpg_decode method and bounce it around the screen with the bitmap method.

    bigbuckbunny.jpg (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org
"""

import random
import time
import st7789
import tft_config
from machine import freq

BITMAP_SIZE = const(128)
COLUMNS_IDX = const(1)
ROWS_IDX = const(2)

tft = tft_config.config(1)

def main():

    '''
    Decode and draw jpg on display
    '''

    try:
        tft.init()
        width = tft.width()
        height = tft.height()

        jpg_filename = f'bigbuckbunny-{width}x{height}.jpg'

        tft.jpg(jpg_filename, 0, 0)     # Draw full screen jpg
        tft.show(True)                  # Show the framebuffer and wait for it to finish
        tft.fill(st7789.BLACK)          # Clear the framebuffer
        time.sleep(1)                   # Wait a second

        # Decode the center 128x128 portion of the jpg and save (bitmap_bytes, width,height) tuple
        column = width // 2 - BITMAP_SIZE //2
        row = height // 2 - BITMAP_SIZE //2
        bitmap = tft.jpg_decode(jpg_filename, column, row, BITMAP_SIZE, BITMAP_SIZE)

        xd = 1
        yd = 1

        while True:
            tft.bitmap(bitmap, column, row)    # Draw the bitmap
            tft.show(True)                     # Show the framebuffer and wait for it to finish

            # Clear the area where the bitmap was
            tft.fill_rect(column, row, bitmap[COLUMNS_IDX], bitmap[ROWS_IDX], st7789.BLACK)

            # Update the position to bounce the bitmap around the screen
            column += xd
            if column in [0, width - bitmap[COLUMNS_IDX]]:
                xd = -xd

            row += yd
            if row in [0, height - bitmap[ROWS_IDX]]:
                yd = -yd


    finally:
        tft.deinit()    # Deinitialize the display or it will cause a crash on the next run

main()
