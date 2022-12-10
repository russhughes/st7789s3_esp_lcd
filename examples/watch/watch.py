""""
watch.py - Analog Watch Display using jpg for the face and filled polygons for the hands
    Requires face_{width}x{height}.jpg in the same directory as this script. See the create_face.py
    script for creating a face image for a given sized display.

    Previous version video: https://youtu.be/NItKb6umMc4
"""

import utime
import math
import st7789
import tft_config


tft = tft_config.config(1)


def hand_polygon(length, radius):
    return [
        (0, 0),
        (-radius, radius),
        (-radius, int(length * 0.3)),
        (-1, length),
        (1, length),
        (radius, int(length * 0.3)),
        (radius, radius),
        (0,0)
    ]


def main():
    '''
    Draw analog watch face and update time
    '''

    try:
        # enable display
        tft.init()
        width = tft.width()
        height = tft.height()
        radius = min(width, height)         # face is the smaller of the two
        ofs = (width - radius) // 2         # offset from the left to center the face
        center_x = radius // 2 + ofs - 1    # center of the face horizontally
        center_y = radius // 2 - 1          # center of the face vertically

        # load and decode the watch face background
        face_file = f'face_{width}x{height}.jpg'
        face = tft.jpg_decode(face_file)

        # create the polygons for the hour, minute and second hands
        # polygons must be closed convex polygons or bad things(tm) happen.

        second_len = int(radius * 0.65 / 2)
        second_poly = hand_polygon(second_len, 2)

        minute_len = int(radius * 0.6 / 2)
        minute_poly = hand_polygon(minute_len, 2)

        hour_len = int(radius * 0.5 / 2)
        hour_poly = hand_polygon(hour_len, 3)

        # constants for calculating hand angles.
        pi_div_6 = math.pi/6
        pi_div_30 = math.pi/30
        pi_div_360 = math.pi/360
        pi_div_1800 = math.pi/1800
        pi_div_2160 = math.pi/2160

        while True:
            # draw the watch face
            tft.bitmap(face, 0, 0)

            # save the current time in seconds so we can determine when
            # when to update the display.
            last = utime.time()

            # get the current hour, minute and second
            _, _, _, hour, minute, second, _, _ = utime.localtime()

            # constrain hours to 12 hour time
            hour %= 12

            # calculate the angle of the hour hand in radians
            hour_ang = (
                (hour * pi_div_6) +
                (minute * pi_div_360) +
                (second * pi_div_2160))

            # calculate the angle of the minute hand in radians
            minute_ang = ((minute*pi_div_30)+(second*pi_div_1800))

            # calculate the angle of the second hand on radians
            second_ang = (second*pi_div_30)

            # draw and fill the hour hand polygon rotated to hour_ang
            tft.fill_polygon(hour_poly, center_x, center_y, st7789.BLACK, 255, hour_ang)

            # draw and fill the minute hand polygon rotated to minute_ang
            tft.fill_polygon(minute_poly, center_x, center_y, st7789.BLACK, 255, minute_ang)

            # draw and fill the second hand polygon rotated to second_ang
            tft.fill_polygon(second_poly, center_x, center_y, st7789.RED, 255, second_ang)

            # draw the hub again to cover up the second hand
            tft.fill_circle(center_x, center_y, 5, st7789.BLACK)

            # update the display
            tft.show(True)

            # wait until the current second changes
            while last == utime.time():
                utime.sleep_ms(50)

    finally:
        tft.deinit()

main()
