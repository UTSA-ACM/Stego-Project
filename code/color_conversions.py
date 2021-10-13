import colorsys
import struct
import math
from functools import wraps
import re


def _rgb_fraction_to_whole(r, g, b):
    return list(map(lambda x: x*255, [r, g, b]))


def _rgb_whole_to_fraction(r, g, b):
    return list(map(lambda x: x/255, [r, g, b]))


def normalized_rgb_to_hsv(r, g, b, *args, **kwargs):
    hsv_percentages = colorsys.rgb_to_hsv(*_rgb_whole_to_fraction(r, g, b))
    normalized_hsv_amounts = [round(hsv_percentages[0] * 360), *map(lambda x: x*100, hsv_percentages[1:])]

    # custom Hue component - only multiples of 3
    normalized_hsv_amounts[0] //= 60
    return *normalized_hsv_amounts, *args


def normalized_hsv_to_rgb(h, s, v, *args, **kwargs):
    # uses 120 instead of 360 due to the custom
    rgb_percentages = colorsys.hsv_to_rgb(h/60, s/100, v/100)
    return *_rgb_fraction_to_whole(*rgb_percentages), *args


def normalized_rgb_to_hls(r, g, b, *args, **kwargs):
    hsl_percentages = colorsys.rgb_to_hls(*_rgb_whole_to_fraction(r, g, b))
    normalized_rgb_values = [round(hsl_percentages[0] * 360), *map(lambda x: x*100, hsl_percentages[1:])]
    return *normalized_rgb_values, *args


def normalized_hls_to_rgb(h, l, s, *args, **kwargs):
    rgb_percentages = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return *_rgb_fraction_to_whole(*rgb_percentages), *args


def normalized_rgb_to_yiq(r, g, b, *args, **kwargs):
    # rounds the float and then turns it into bits
    yiq_percentages = colorsys.rgb_to_yiq(*_rgb_whole_to_fraction(r, g, b))
    return *yiq_percentages, *args


def normalized_yiq_to_rgb(y, i, q, *args, **kwargs):
    rgb_percentages = colorsys.yiq_to_rgb(y, i, q)
    return *_rgb_fraction_to_whole(*rgb_percentages), *args


def _default_rgb_transform(x, shift=122):
    return (x + shift) % 255


def _default_rgb_untransform(x, shift=122):
    return (x - shift) % 255


def normalized_rgb_to_rgbtransformed(r, g, b, *args,
        transformer=_default_rgb_transform, **kwargs):
    return *map(transformer, [r, g, b]), *args


def normalized_rgbtransformed_to_rgb(r, g, b, *args, 
        untransformer=_default_rgb_untransform, **kwargs):
    return *map(untransformer, [r, g, b]), *args


def color_converter(func):

    def _color_converter_wrapper(self, colors, func, in_converter,
            out_converter, raw_output=False, **kwargs):
        # converts input to output
        converted_output = in_converter(*colors)

        # runs the function with the new values
        converted_output = func(self, converted_output, **kwargs)

        # then converts back to the original format if colors are expected
        if not raw_output:
            unconverted_output = out_converter(*converted_output, **kwargs)
        # else just return the raw return values
        else:
            return converted_output

        return unconverted_output

    @wraps(func)
    def inner(self, colors, input_scheme=None, output_scheme=None, raw_output=False, **kwargs):
        # tries to get the inputs
        if not input_scheme:
            # assigns the input scheme to the processors scheme
            try:
                input_scheme = self.input_scheme
            # else defaults to RGB
            except AttributeError:
                input_scheme = "rgb"

        if not output_scheme:
            # assigns the output to the processors scheme
            try:
                output_scheme = self.output_scheme
            except AttributeError:
                output_scheme = "rgb"

        # if the input/output are the same
        if input_scheme == output_scheme:
            return func(self, colors, **kwargs)

        # just uses locals so there don't have to be color_formats**2 if
        # statements
        in_converter_str = "normalized_" + input_scheme + "_to_" + output_scheme
        out_converter_str = "normalized_" + output_scheme + "_to_" + input_scheme 
        try:
            in_converter = globals()[in_converter_str]
            out_converter = globals()[out_converter_str]
        except KeyError:
            # TODO
            # conversions = set(re.search)
            raise ValueError(f"Input and output color schemes not in valid schemes")

        # returns the function wrapped in the converters
        return _color_converter_wrapper(self, colors, func, in_converter, out_converter, raw_output=raw_output, **kwargs)

    return inner
