"""
toasters_jpg.py

    An example using a jpg sprite map to draw sprites on T-Display.  This is an older version of the
    toasters.py and tiny_toasters example.  It uses the jpg_decode() method to grab a bitmap of each
    sprite from the toaster.jpg sprite sheet.

    youtube video: https://youtu.be/0uWsjKQmCpU

    spritesheet from CircuitPython_Flying_Toasters
    https://learn.adafruit.com/circuitpython-sprite-animation-pendant-mario-clouds-flying-toasters
"""

import time
import random
import tft_config
import st7789

tft = tft_config.config(0)

class toast():
    '''
    toast class to keep track of a sprites locaton and step
    '''

    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.steps = len(sprites)
        self.x = x
        self.y = y
        self.step = random.randint(0, self.steps-1)
        self.speed = random.randint(2, 5)

    def move(self):
        if self.x <= 0:
            self.speed = random.randint(2, 5)
            self.x = tft.width()-64

        self.step += 1
        self.step %= self.steps
        self.x -= self.speed


def main():
    '''
    Draw and move sprite
    '''

    try:
        # enable display and clear screen
        tft.init()
        tft.fill(st7789.BLACK)
        tft.show()

        sprite_width = 64
        sprite_height = 64

        # grab each sprite from the toaster.jpg sprite sheet
        print("Loading sprites...")
        t1, _, _ = tft.jpg_decode('toaster.jpg', 0, 0, sprite_width, sprite_height)
        t2, _, _ = tft.jpg_decode('toaster.jpg', sprite_width, 0, sprite_width, sprite_height)
        t3, _, _ = tft.jpg_decode('toaster.jpg', sprite_width*2, 0, sprite_width, sprite_height)
        t4, _, _ = tft.jpg_decode('toaster.jpg', 0, sprite_height, sprite_width, sprite_height)
        t5, _, _ = tft.jpg_decode('toaster.jpg', sprite_width, sprite_height, sprite_width, sprite_height)
        print("Sprites loaded")

        TOASTERS = [t1, t2, t3, t4]
        TOAST = [t5]

        sprites = [
            toast(TOASTERS, tft.width() - sprite_width, 0),
            toast(TOAST, tft.width() - sprite_width, tft.height() // 3),
            toast(TOASTERS, tft.width() - sprite_width, tft.height() // 3 * 2)
        ]

        # move and draw sprites
        while True:
            for man in sprites:
                bitmap = man.sprites[man.step]

                tft.fill_rect(
                    man.x+sprite_width-man.speed,
                    man.y,
                    man.speed,
                    sprite_height,
                    st7789.BLACK)

                man.move()

                if man.x > 0:
                    tft.blit_buffer(bitmap, man.x, man.y, sprite_width, sprite_height)
                else:
                    tft.fill_rect(
                        0,
                        man.y,
                        sprite_width,
                        sprite_height,
                        st7789.BLACK)

            tft.show()
            time.sleep(0.05)

    finally:
        tft.deinit()


main()
