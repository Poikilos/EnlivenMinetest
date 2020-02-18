#!/usr/bin/env python
"""
Installation: place this in plug-ins and mark executable, such as:
~/.gimp-2.8/plug-ins/
(To find your plug-in paths, open GIMP, click Edit, Preferences,
Folders, Plug-ins)

Upgrading: You must restart GIMP if you upgrade the plugin.

Development Notes:
- In GIMP, see Help, Prodedure browser to view GIMP's own documentation.
  Python differences from regular API
  (See https://www.youtube.com/watch?v=YHXX3KuB23Q):
  - Change dashes to underscores
  - Change -1 to None
  - do not pass run mode
- Making a copy of the pixels would be much faster if repetitive get
  pixel calls are necessary.

"""

import math
import sys
from itertools import chain

from gimpfu import *  # by convention, import *


def fdist(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def idist(pos1, pos2):
    fpos1 = [float(i) for i in pos1]
    fpos2 = [float(i) for i in pos2]
    return fdist(fpos1, fpos2)


def find_opaque_pos(near_pos, threshold=255, max_rad=None, drawable=None, w=None, h=None):
    """
    Sequential arguments:
    near_pos -- This location, or the closest location to it meeting
    criteria, is the search target.
    Keyword arguments:
    threshold -- (0 to 255) If the pixel's alpha is this or higher, get
    it (the closest in location to near_pos).
    """
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
    for i in range(0, max_rad + 1):
        left = near_pos[0] - i
        right = near_pos[0] + i
        top = near_pos[1] - i
        bottom = near_pos[1] + i
        # For each side of the square, only use positions within the
        # circle:
        for x in chain(range(left, right + 1), range(left, right + 1)):
            if x < 0:
                continue
            if x > w:
                continue
            for y in (top, bottom):
                # top row of square
                if y < 0:
                    continue
                if y > h:
                    continue
                pos = (x, y)
                dist = idist(near_pos, pos)
                if dist <= float(i) - epsilon:
                    all_channels, pixel = pdb.gimp_drawable_get_pixel(
                        drawable,
                        pos[0],
                        pos[1]
                    )
                    if pixel[3] >= threshold:
                        return pos
        # For each side of the square (continued)
        for y in chain(range(top+1, bottom), range(top+1, bottom)):
            if y < 0:
                continue
            if y > h:
                continue
            # purposely exclude corners (done in previous loop)
            for x in (left, right):
                if x < 0:
                    continue
                if x > w:
                    continue
                # top row of square
                pos = (x, y)
                dist = idist(near_pos, pos)
                if dist <= float(i) - epsilon:
                    all_channels, pixel = pdb.gimp_drawable_get_pixel(
                        drawable,
                        pos[0],
                        pos[1]
                    )
                    if pixel[3] >= threshold:
                        return pos
    return None


def extend(threshold=254, make_opaque=False):
    """
    Keyword arguments:
    threshold -- (0 to 255) If the pixel's alpha is this or lower,
    change its color
    make_opaque -- Make the pixel within the threshold opaque. This is
    normally for preparing to convert images to indexed color, such as
    Minetest wield_image.
    """
    # exists, x1, y1, x2, y2 = \
    #     pdb.gimp_selection_bounds(self.img)
    img = gimp.image_list()[0]
    drawable = pdb.gimp_image_active_drawable(img)
    w = pdb.gimp_image_width(img)
    h = pdb.gimp_image_height(img)
    new_channels = 3
    if make_opaque:
        new_channels = 4
    for x in range(w):
        for y in range(h):
            all_channels, pixel = pdb.gimp_drawable_get_pixel(drawable, x, y)
            # if all([p == q for p, q in zip(pixel, color_to_edit)]):
            opaque_pos = find_opaque_pos(x, y, drawable=drawable, w=w, h=h)
            pdb.gimp_drawable_set_pixel(drawable, x, y, new_channels, new_color)


def remove_layer_halo():
    extend(threshold=0, make_opaque=True)
    pdb.gimp_displays_flush()  # update the image


# See https://jacksonbates.wordpress.com/2015/09/14/python-fu-6-accepting-user-input/
register(
    "python_fu_remove_halo",
    "Remove Halo",
    "Remove alpha",
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Redo the edge...",
    "RGBA",  # RGB* would mean with or without alpha.
    [
        (PF_SPINNER, "threshold", "Minimum alpha to fix", 254, (0, 255, 1)),
        (PF_BOOL, "make_opaque", "Make the fixed parts opaque.", True),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    remove_layer_halo, menu="<Image>/Layer,Remove Halo"
)

main()
