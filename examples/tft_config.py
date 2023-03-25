""" LilyGo T-DISPLAY-S3 170x320 ST7789 display """

from machine import freq
import st7789

TFA = 0
BFA = 0

freq(240_000_000)

def config(rotation=0, options=0):
    return st7789.ST7789(
        170,
        320,
        48, 47, 46, 45, 42, 41, 40, 39,
        wr=8,
        rd=9,
        reset=5,
        dc=7,
        cs=6,
        backlight=38,
        power=15,
        rotation=rotation,
        options=options)
