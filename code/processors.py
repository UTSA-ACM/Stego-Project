from abc import ABC, abstractmethod
from PIL import Image
from PIL.ImageFile import ImageFile

from bitarray import bitarray

from utils import color_int_to_bitarray, color_bitarray_to_int
from color_conversions import color_converter


class BaseStegoProcessor(ABC):
    #################################
    # PUBLIC METHODS (TO IMPLEMENT) #
    #################################
    @abstractmethod
    def hide(self, data):
        ...

    @abstractmethod
    def extract(self, data):
        ...


class BaseStegoIO(ABC):
    def __init__(self, img):
        # checks if it is an image already, else loads it
        if isinstance(img, ImageFile):
            self.img = img
        # else it is an image path
        else:
            self.img = Image.open(img)

    @abstractmethod
    def read(self):
        ...

    @abstractmethod
    def write(self):
        ...


class LSBStegoProcessor(BaseStegoProcessor):
    def __init__(self, color_bits, input_scheme="rgb", output_scheme="rgb"):
        self.color_bits = color_bits
        self.input_scheme = input_scheme
        self.output_scheme = output_scheme

    @color_converter
    @color_int_to_bitarray
    @color_bitarray_to_int
    def _hide_in_colors_lsb(self, colors, msg, **kwargs):
        new_colors = []
        for color, bits in zip(colors, self.color_bits):
            # iterates over the bits, last to first
            for bit in range(-1, -(bits+1), -1):
                # tries to write the next message bit
                try:
                    color[bit] = next(msg)
                # if the message is over
                except StopIteration:
                    break

            new_colors.append(color)

        return new_colors

    @color_converter
    @color_int_to_bitarray
    def _extract_colors_lsb(self, colors, **kwargs):
        msg = bitarray()
        for color, bits in zip(colors, self.color_bits):
            msg += color[-1:-(bits+1):-1]
        return msg

    def hide(self, msg, data, **kwargs):
        # converts the tuple back to ints
        for color_tuple in data:
            val = self._hide_in_colors_lsb(color_tuple, msg=msg,
                    raw_output=False, **kwargs)
            yield val

            # yield self._hide_in_colors_lsb(color_tuple, msg=msg,
            #         raw_output=False, **kwargs)

    def extract(self, data, **kwargs):
        msg = bitarray()

        for color_tuple in data:
            msg += self._extract_colors_lsb(color_tuple, raw_output=True, **kwargs)

        return msg


class RBGAStegoIO(BaseStegoIO):
    def read(self):
        return self.img.getdata()

    def write(self, new_colors, file_path):
        self.img.putdata(new_colors)
        self.img.save(file_path)


def get_io_class(img):
    # if the img is a string (filepath)
    img = Image.open(img)

    # gets the images mode
    mode = img.mode

    # RBG with Alpha channel
    if mode == "RGBA" or mode == "RGB":
        return RBGAStegoIO(img)
