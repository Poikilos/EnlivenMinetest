#!/usr/bin/env python
"""
For each pixel where the alpha is below the threshold, get a new color
using the nearest opaque pixel.
"""

import math
import sys
from itertools import chain
import time

from gimpfu import *  # by convention, import *


def fdist(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def idist(pos1, pos2):
    fpos1 = [float(i) for i in pos1]
    fpos2 = [float(i) for i in pos2]
    return fdist(fpos1, fpos2)

def square_shape(pos, rad):
    left = pos[0] - rad
    right = pos[0] + rad
    top = pos[1] - rad
    bottom = pos[1] + rad
    x = left
    y = top
    v_count = left - right + 1
    h_count = bottom - (top + 1)
    ender = v_count * 2 + h_count * 2
    ss_U = 0
    ss_D = 1
    ss_L = 2
    ss_R = 3
    d = ss_R
    while True:
        yield (x,y)
        if d == "r":
            x += 1
            if x > right:
                x = right
                y += 1
                d = ss_D
        elif d == ss_D:
            y += 1
            if y > bottom:
                y = bottom
                x -= 1
                d = ss_L
        elif d == ss_L:
            x -= 1
            if x < left:
                x = left
                y -= 1
                d = ss_U
        else:
            y -= 1
            if y < top:
                y = top
                break



def find_opaque_pos(near_pos, good_minimum=255, max_rad=None, drawable=None, w=None, h=None):
    """
    Sequential arguments:
    near_pos -- This location, or the closest location to it meeting
    criteria, is the search target.
    Keyword arguments:
    good_minimum -- (0 to 255) If the pixel's alpha is this or higher,
    get it (the closest in location to near_pos).
    """
    if good_minimum < 0:
        good_minimum = 0
    epsilon = sys.float_info.epsilon
    rad = 0
    if drawable is None:
        img = gimp.image_list()[0]
        drawable = pdb.gimp_image_active_drawable(img)
        w = pdb.gimp_image_width(img)
        h = pdb.gimp_image_height(img)
    if max_rad is None:
        max_rad = 0
        side_distances = [
            abs(0 - near_pos[0]),
            abs(w - near_pos[0]),
            abs(0 - near_pos[1]),
            abs(h - near_pos[1]),
        ]
        for dist in side_distances:
            if dist > max_rad:
                max_rad = dist
    print("find_opaque_pos({},...) # max_rad:{}".format(near_pos, max_rad))
    for rad in range(0, max_rad + 1):
        left = near_pos[0] - rad
        right = near_pos[0] + rad
        top = near_pos[1] - rad
        bottom = near_pos[1] + rad
        # For each side of the square, only use positions within the
        # circle:
        y = top
        count = 0
        next_count = (right + 1) - left
        for x in chain(range(left, right + 1), range(left, right + 1)):
            # if x == right:
            if count >= next_count:
                y = bottom
            count += 1
            if x < 0:
                continue
            if x >= w:
                continue
            # top row of square
            if y < 0:
                continue
            if y >= h:
                break
            pos = (x, y)
            dist = idist(near_pos, pos)
            if dist <= float(rad) - epsilon:
                print("  navigating verticals {}".format(pos))
                all_channels, pixel = pdb.gimp_drawable_get_pixel(
                    drawable,
                    pos[0],
                    pos[1]
                )
                if pixel[3] >= good_minimum:
                        return pos
            else:
                print("  navigating verticals {} SKIPPED ({} > {})".format(pos, dist, rad))
                pass
        # For each side of the square (continued)
        count = 0
        next_count = bottom - (top + 1)
        for y in chain(range(top+1, bottom), range(top+1, bottom)):
            # if y == bottom - 1:
            if count >= next_count:
                x = right
            count += 1
            if y < 0:
                continue
            if y >= h:
                continue
            # purposely exclude corners (done in previous loop)
            if x < 0:
                continue
            if x >= w:
                continue
            # top row of square
            pos = (x, y)
            dist = idist(near_pos, pos)
            if dist <= float(rad) - epsilon:
                print("  navigating verticals {} SKIPPED ({} > {})".format(pos, dist, rad))
                all_channels, pixel = pdb.gimp_drawable_get_pixel(
                    drawable,
                    pos[0],
                    pos[1]
                )
                if pixel[3] >= good_minimum:
                    return pos
            else:
                print("  navigating verticals {} SKIPPED".format(pos))
                pass
    return None


def extend(image=None, drawable=None, minimum=1, maximum=254, make_opaque=False, good_minimum=255):
    """
    Keyword arguments:
    minimum -- (0 to 255) Only edit pixels with at least this for alpha.
    maximum -- (0 to 254) Only edit pixels with at most this for alpha.
    make_opaque -- Make the pixel within the range opaque. This is
    normally for preparing to convert images to indexed color, such as
    Minetest wield_image.
    """
    if maximum < 0:
        maximum = 0
    if minimum < 0:
        minimum = 0
    if maximum > 254:
        maximum = 254
    # exists, x1, y1, x2, y2 = \
    #     pdb.gimp_selection_bounds(self.image)
    if image is None:
        image = gimp.image_list()[0]
    if drawable is None:
        drawable = pdb.gimp_image_active_drawable(image)
    w = pdb.gimp_image_width(image)
    h = pdb.gimp_image_height(image)
    new_channels = 4
    # ^ new_channels must match the destination channel count,
    # or an ExecutionError occurs.
    if make_opaque:
        new_channels = 4
    print("Size: {}".format((w, h)))
    total_f = float(w * h)
    count_f = 0.0
    # ok = True
    for y in range(h):
        # if not ok:
        #     break
        for x in range(w):
            # if count_f is None:
            count_f = float(y) * float(w) + float(x)
            # print("checking {}".format(pdb.gimp_drawable_get_pixel(drawable, x, y)))
            all_channels, pixel = pdb.gimp_drawable_get_pixel(drawable, x, y)
            if (pixel[3] >= minimum) and (pixel[3] <= maximum):
                # if all([p == q for p, q in zip(pixel, color_to_edit)]):
                pos = (x, y)
                opaque_pos = find_opaque_pos((x, y), drawable=drawable, w=w, h=h, good_minimum=good_minimum)
                if (opaque_pos is not None):
                    if opaque_pos == pos:
                        msg = "Uh oh, got own pos when checking for better color than {}...".format(pixel)
                        print(msg)
                        # pdb.gimp_message(msg)
                        gimp.progress_init(msg)
                        gimp.progress_update(0.0)
                        time.sleep(10)
                        # ok = False
                        continue
                    all_channels, new_pixel = pdb.gimp_drawable_get_pixel(drawable, opaque_pos[0], opaque_pos[1])
                    if new_pixel != pixel:
                        if make_opaque:
                            new_pixel = (new_pixel[0], new_pixel[1], new_pixel[2], 255)

                        # print("Changing pixel at {} from {} to {}".format((x, y), pixel, new_pixel))
                        print("Changing pixel at {} using color from {}".format((x, y), opaque_pos))
                        pdb.gimp_drawable_set_pixel(drawable, x, y, new_channels, new_pixel)
                    else:
                        # msg = "Uh oh, got own {} color {} at {} when checking for color at better position than {}...".format(pixel, new_pixel, opaque_pos, pos)
                        # print(msg)
                        # pdb.gimp_message(msg)
                        # gimp.progress_init(msg)
                        # gimp.progress_update(count_f / total_f)
                        # count_f = None
                        # time.sleep(10)
                        # return
                        # continue
                        pass
                else:
                    msg = "Uh oh, the image has no pixels at or above the minimum good alpha."
                    print(msg)
                    pdb.gimp_message(msg)
                    pdb.gimp_drawable_update(drawable,0,0,drawable.width,drawable.height)
                    return
            if count_f is not None:
                # count_f += 1.0
                gimp.progress_update(count_f / total_f)
    pdb.gimp_drawable_update(drawable,0,0,drawable.width,drawable.height)


def remove_layer_halo(image, drawable, minimum, maximum, good_minimum, make_opaque):
    gimp.progress_init("This may take a while...")
    print("options: {}".format((str(image), str(drawable), str(minimum), str(maximum), str(make_opaque), str(good_minimum))))
    extend(image=image, drawable=drawable, minimum=minimum, maximum=maximum, make_opaque=make_opaque, good_minimum=good_minimum)
    print("updating image...")
    pdb.gimp_displays_flush()  # update the image; doesn't work
    print("done (remove_layer_halo)")


# See https://www.youtube.com/watch?v=uSt80abcmJs
register(
    "python_fu_remove_halo",
    "Remove Halo",
    "Remove alpha",
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Remove Halo",  # caption
    "RGBA",  # RGB* would mean with or without alpha.
    [
        (PF_IMAGE, "image", "Current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_SPINNER, "minimum", "Minimum alpha to fix (normally 1)", 1, (0, 255, 1)),
        (PF_SPINNER, "maximum", "Maximum alpha to fix (normally 254 unless less damaged)", 254, (0, 255, 1)),
        (PF_SPINNER, "good_minimum", "Find a nearby color >= this (usually maximum+1).", 255, (0, 255, 1)),
        (PF_TOGGLE, "make_opaque", "Make the fixed parts opaque.", True),
    ],
    [], # results
    remove_layer_halo,
    menu="<Image>/Layer"
)

main()
