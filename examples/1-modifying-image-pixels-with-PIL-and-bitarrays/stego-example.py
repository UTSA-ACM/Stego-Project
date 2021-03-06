# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17O65GvRYH4h5mVKMkPTosWbcbYr-PLsF
"""

# this is how you can upload your test files
# I just used a 4x4 (16 pixel) white image to really show the color differences
from google.colab import files

uploaded = files.upload()

# you can install the bitarray package using this
!pip install bitarray

# on your own computer with Python, you can install PIL and bitarray with:
# pip install pillow
# pip install bitarray

# we are now importing the Python Imaging Library (PIL) to manipulate images, and the bitarray class to more easily convert to and from raw bits
from PIL import Image
from bitarray import bitarray

# here we define the file names we are loading and writing to, and open the image
OLD_FILE = "./white-4-by-4.png"
NEW_FILE = "./new-white-4-by-4.png"

img = Image.open(OLD_FILE)

# this example shows how you can modify colors in PIL

# this is the list that will contain our new color triplets (the RGB values)
new_data = []

# NOTE: white RGB vals: [255, 255, 255]
# this modifies the image to have only 0,255,255 rgb values
for rgb_pair in img.getdata():
  # explicity defines the RGB values
  red = rgb_pair[0]
  green = rgb_pair[1]
  blue = rgb_pair[2]

  # sets our new red to have no red tint
  new_red = 0
  new_rgb_values = (new_red, green, blue)

  # adds uur new RGB color to our list
  new_data.append(new_rgb_values)

# lastly, we set the first pixel to pure black
new_data[0] = (0, 0, 0)

# this example now does the exact same thing as the last example, but this time
# we are modifying the color values bit by bit

new_data = []

# here we can define how many bits we want to 0 out (make 0)
# For example, if we made this 2, the last bit in each color would be 0
LSB_BITS_TO_ZERO = 2

for rgb_pair in img.getdata():
  red = rgb_pair[0]
  green = rgb_pair[1]
  blue = rgb_pair[2]

  # create the bitarrays (the arrays of bits, the 1s and 0s that make up computer values)
  # NOTE: the 'format(COLOR, "08b")' creates a string of bits that a bitarray can interpret
  # if you're confused about it, just uncomment this:
  # print(f"Here's my formatted binary red: {format(red, '08b')}")
  red_ba = bitarray(format(red, "08b"))
  green_ba = bitarray(format(green, "08b"))
  blue_ba = bitarray(format(blue, "08b"))

  # iterates (goes over) each bitarray, making the last "LSB_BITS_TO_ZERO" bits 0 in each bitarray
  for ba in [red_ba, green_ba, blue_ba]:

    # for each bit to zero out, we do so (the range loop starts at 1 and goes to LSB_BITS_TO_ZERO)
    for bit_to_zero in range(1, LSB_BITS_TO_ZERO+1):
  
      # remember, negative list indexes in python mean going backwards in the list
      # think of it like the list wraps around, so the -1 is the last element, -2 is the 2nd to last, etc.
      # if we didn't make bit to zero negative, we would instead be modifying the most significant bit (check out what happens when you do this!)
      ba[-bit_to_zero] = 0

  # here we ust print off the bitarray to confirm we've done everything right
  print(f"red ba: {red_ba}")

  # now we can convert the bitarrays back to integers
  new_rgb_value = []
  for ba in [red_ba, green_ba, blue_ba]:
    
    # this is super convoluted, so dont worry about it too much
    # Basically, we make the bitarray bytes, then load the bytes into an integer
    new_color_int = int.from_bytes(ba.tobytes(), "big")
    new_rgb_value.append(new_color_int)

  # lastly, we can check our new RGB value and then add it to the list of image pixels
  print(f"Here's my modified pixel: Red: {new_rgb_value[0]} Blue: {new_rgb_value[1]} Blue: {new_rgb_value[2]}")

  # NOTE: we just have to make this a tuple (basically a list that you can't modify)
  # this doesn't really change anything, just a PIL quirk
  new_data.append(tuple(new_rgb_value))

# and to check all your work at once, just uncomment these two lines to see the final image pixels
# print("\n\nHere's my image data!\n")
# print(new_data)