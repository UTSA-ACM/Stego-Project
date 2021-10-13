from PIL import Image
import colorsys
import itertools
import more_itertools
from functools import wraps
from random import randint
import struct

from bitarray import bitarray


def check_str_is_binary(bin_str):
    return set("10") == set(bin_str)


def stego_hsv_lsb(cover_file, msg, r_hid=1, g_hid=1, b_hid=1):
    # loads the image
    img = Image.open(cover_file)

    # creates the palettes with nested RGB lists
    palette = img.getpalette()
    # palette = [palette[i:i+3] for i in range(0, len(palette), 3)]

    # iterates over the palette
    for r, g, b in itertools.zip_longest(*([iter(palette)] * 3)):
        r_bin, g_bin, b_bin = map(lambda x: bin(x)[2:], [r,g,b])
        # hides each of the colors
        for color_bin, bits in zip([r_bin, g_bin, b_bin], [r_hid, g_hid, b_hid]):
            # hides the number of bits
            for bit in range(bits):
                color_bin[bit]


def binary_to_text(bin_arr):
    return "".join([chr(char) for char in bin_arr.tobytes()])


def message_generator(data=None):
    # if there is no message, assumes it should generate random noise
    if not data:
        while True:
            yield randint(0, 1)

    # else data to be generated exists
    else:
        # checks if the string is already in binary
        if check_str_is_binary(data):
            # yields each digit one by one
            for bit in data:
                yield int(bit)
        # else it is a normal string
        else:
            # creates the bit array and returns it
            bin_arr = bitarray()
            bin_arr.frombytes(bytes(data, "ascii"))
            for bit in bin_arr:
                print(bit)
                yield bit


def color_int_to_bitarray(func):
    def inner(self, colors, *args, **kwargs):
        # converts colors to bitarrays
        bitarray_colors = []
        for color in colors:
            # checks if it is just a float ending in .0
            if int(color) == color:
                color = int(color)

            try:
                bitarray_colors.append(bitarray(format(color, "08b")))
            except ValueError:
                print("Currently, bit manipulations are not supported with floating point numbers arising from color conversions. Continuing...")
                bitarray_colors.append(color)

        # runs the function to modify the colors
        new_colors = func(self, bitarray_colors, *args, **kwargs)

        return new_colors

    return inner


def color_bitarray_to_int(func):
    def inner(self, colors, *args, **kwargs):
        # runs function and gets new bitarray colors
        bitarray_colors = func(self, colors, *args, **kwargs)

        # converts bitarrays to colors
        int_colors = tuple([int.from_bytes(ba.tobytes(), "little") for ba in bitarray_colors])

        return int_colors

    return inner


def DEPRECATED_set_int_bit(val, index, new_bit):
    mask = 1 << index
    val &= ~mask
    if new_bit:
        val |= mask
    return val


def DEPRECATED_get_int_bit(val, index):
    return 1 if val & (1 << index) else 0


def DEPRECATED_float_to_int(f):
    return struct.unpack(">l", struct.pack(">f", round(f, 5)))[0]


def DEPRECATED_int_to_float(i):
    return round(struct.unpack(">f", struct.pack(">l", i))[0], 5)
