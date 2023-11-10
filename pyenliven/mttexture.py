'''
Transpose an animation from type="vertical_frames" to type="sheet_2d"

Usage:
recompose-anim <path> <aspect_w> <aspect_h> <frames_w> <frames_h> <length>

Options:
path            The image file.
aspect_w        The width of each frame in the multi-frame file.
aspect_h        The height of each frame in the multi-frame file.
frames_w        The number of frames across the new image should be.
frames_h        The number of frames down the new image should be.
length          Total length of the animation in seconds (which is the
                necessary argument when type="vertical_frames"). This
                value is only required since this program shows Lua in
                standard output: The value will be automatically
                converted to a frame_length (single-frame time in
                seconds) argument for the node which is the argument
                necessary when type="sheet_2d".

Examples:
# [Mod] Mom and Pop Furniture [mapop]:
recompose-anim mp_channel_rainbow.png 64 48 8 8 2
recompose-anim mp_channel_cube.png 40 40 5 5 3
recompose-anim mp_channel_blast.png 64 64 8 8 5
# ^ 5 5 is optional, but ideal since 1200/48 is 25 as square textures
#   are efficient (but power of 2 textures such as 512x512 are better
#   and more efficient on older video cards such as on old iPhones)
'''
from __future__ import print_function
import sys
import os

from collections import OrderedDict
from PIL import Image
from pprint import pformat


def echo0(*args, **kwargs):
    dst = sys.stderr
    if 'file' in kwargs:
        dst = kwargs['file']
        del kwargs['file']
    print(*args, file=dst, **kwargs)


def usage():
    echo0(__doc__)
    echo0()


option_metas = [
    {
        'name': "path",
    },
    {
        'name': "aspect_w",
        'type': "int",
    },
    {
        'name': "aspect_h",
        'type': "int",
    },
    {
        'name': "frames_w",
        'type': "int",
    },
    {
        'name': "frames_h",
        'type': "int",
    },
    {
        'name': "length",
        'type': "int",
    },
]


class Framer:
    def __init__(self):
        self.frames = []

    def load_vertical_strip(self, image, aspect_w, aspect_h):
        results = OrderedDict()
        results['-- in_count'] = 0
        # results['-- out_count'] = 0  # set by save methods instead.
        w, h = image.size
        inverse_ar = float(aspect_h) / float(aspect_w)
        # ^ inverse aspect ratio
        frame_h = int(round(inverse_ar*w))
        if h % frame_h != 0:
            raise ValueError(
                "Height {} of image is not evenly divisible by the"
                " calculated frame_height {}--calculated using"
                " frame_height = (aspect_h/aspect_w)*image_w = ({}/{})*{}"
                "".format(h, frame_h, aspect_h, aspect_w, w)
            )
        top = 0
        left = 0
        right = w  # exclusive
        bottom = top + frame_h  # exclusive
        while top < h:
            frame = image.crop((left, top, right, bottom))
            results['-- in_count'] += 1
            self.frames.append(frame)
            # results['-- out_count'] += 1
            top += frame_h
            bottom += frame_h
        return results

    def save_sheet_2d(self, path, frames_w, frames_h):
        results = OrderedDict()
        if not self.frames:
            raise RuntimeError("You must load first.")
        frame_w, frame_h = self.frames[0].size
        w = frame_w * frames_w
        h = frame_h * frames_h
        image = Image.new('RGBA', (w, h), 0)
        top = 0
        index = 0
        dest_count = frames_w * frames_h
        time_scale = float(dest_count) / float(len(self.frames))
        if time_scale > 1.0:
            time_scale = 1.0  # just leave some blank
        inv_time_scale = 1.0 / time_scale
        last_dest_frame = 0
        for y_frame in range(frames_h):
            left = 0
            for x_frame in range(frames_w):
                if index >= len(self.frames):
                    # The animation is complete.
                    break
                source_index = int(round(inv_time_scale * float(index)))
                echo0("{} saved as frame {}".format(source_index, index))
                image.paste(self.frames[source_index], (left, top))
                # ^ paste copies alpha (alpha_composite does overlay)
                last_dest_frame = index
                left += frame_w
                index += 1
            top += frame_h
        results['-- out_count'] = last_dest_frame + 1
        image.save(path)
        return results


def recompose_anim(options):
    """Recompose a vertical strip animation
    Convert from Minetest animation type="vertical_frames" to
    type="sheet_2d" (transpose to horizontal then split into rows).

    Args:
        options (dict): Configure how to read and convert the animation.
            For all options, see docstring of transpose-anim Python
            file.

    Returns:
        dict: The values that should be used in the texture table (or
            any of the tiles tables) in the minetest.register_node call.
            Additional values are in comment notation:
            '-- in_count' (the detected input frame count)
            '-- out_count' (the generated output frame count)
    """
    path = options.get('path')
    if path is None:
        raise ValueError("You must specify a path.")
    results = OrderedDict()
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    for option_meta in option_metas:
        name = option_meta['name']
        value = options.get(name)
        if value is None:
            raise ValueError(
                "{} is required.".format(name)
            )
        option_type_name = option_meta.get('type')
        if option_type_name:
            if type(value).__name__ != option_type_name:
                raise ValueError(
                    "{} should be a(n) {} but got {} {}."
                    "".format(name, option_type_name,
                              type(value).__name__, pformat(value))
                )
    framer = Framer()
    img = Image.open(options['path'])
    rgba = img.convert("RGBA")

    load_results = framer.load_vertical_strip(
        rgba,
        options['aspect_w'],
        options['aspect_h'],
    )
    nameNoExt, dotExt = os.path.splitext(options['path'])
    results['name'] = nameNoExt+"_sheet_2d"+dotExt
    load_results.update(framer.save_sheet_2d(
        results['name'],
        options['frames_w'],
        options['frames_h'],
    ))
    # ^ update gets the new '-- out_count'
    results['type'] = "sheet_2d"
    results['frames_w'] = options['frames_w']
    results['frames_h'] = options['frames_h']
    results.update(load_results)  # Add the frame count comment(s)
    results['frame_length'] = options['length'] / load_results['-- in_count']
    # ^ It is the in_count not out_count, since 'length' is based on original
    time_scale = (
        float(load_results['-- out_count'])
        / float(load_results['-- in_count'])
    )
    inv_time_scale = 1.0 / time_scale
    results['frame_length'] = results['frame_length'] * inv_time_scale
    # ^ frame_length should be scaled by the output vs input
    #   (inverse since time becomes longer if frame count became less)
    return results


def main():
    options = {}
    for i, option_meta in enumerate(option_metas):
        argi = i + 1
        if len(sys.argv) <= argi:
            usage()
            sys.stderr.write("Error: You must specify all options. Missing {}"
                  "".format(option_meta['name']))
            missing_count = len(option_metas) - (len(sys.argv) - 1)
            if missing_count > 1:
                echo0(" (and the rest after it above).")
            else:
                echo0(".")
            echo0('- If the texture is used in the mod, you can find'
                  ' potential value(s) for in the Lua file'
                  ' (Use same values as used in register_node).'
                  ''.format())
            return 1
        arg = sys.argv[argi]
        if option_meta.get('type') == "int":
            try:
                arg = int(arg)
            except ValueError:
                usage()
                echo0("Error: {} should be a number but got {}."
                      "".format(option_meta['name'], arg))
                return 1
        options[option_meta['name']] = arg
    if not os.path.isfile(options['path']):
        # Avoid an exception & use CLI-style (pipe & filter) logic
        usage()
        echo0('Error: "{}" does not exist.'.format(options['path']))
        return 1
    results = recompose_anim(options)
    echo0("")
    echo0("-- Patching instructions (change the following arguments in")
    echo0(" the animation table which is in the Tile definition table):")
    echo0("-- Remove:")
    echo0('-        type = "vertical_strip",')
    echo0('-        aspect_w = {},'.format(options['aspect_w']))
    echo0('-        aspect_h = {},'.format(options['aspect_h']))
    echo0('-        length = {},'.format(options['length']))
    frame_length = results['frame_length']
    echo0("-- Add:")
    new_path = results['name']
    del results['name']
    for key, value in results.items():
        if isinstance(value, str):
            print('        {} = "{}",'.format(key, value))
        else:
            print('        {} = {},'.format(key, value))
    print('    frame_length = {},'.format(frame_length))
    print('-- Also (in Tile definition, but outside of animation table)')
    print('--   change texture name (or overwrite original "{}"'
          ''.format(os.path.basename(options['path'])))
    print('-    & keep Lua same) with:')
    print('--     name="{}"'.format(new_path))
    return 0

