# Rowdy Creators Steganography Project
This repository contains all of the project code, examples, documentation,
member contributions, and anything else relevant for the UTSA ACM Rowdy
Creator's Steganography project. If you'd like to get involved, just check out
the https://acmutsa.org/ website and join the Discord, we'd love to have you!

## Repository Structure
- examples: this contains the quick walkthroughs demonstrating concepts that are
  conducted in the meetings. If you have anything useful to add to this, let us
  know!
- code: the main project code. This is the "final product" for the semester
- docs: this contains the documentation for the main project
- samples: this contains several standard sample images to test your code on

## Installation

pipenv install

OR

pip install -r requirements


### To make executable
(must be on the platform you're trying to build for)

pipenv install --dev
pyinstaller stego_lsb.py --onefile

pip install -r requirements-dev.txt
pyinstaller stego_lsb.py --onefile

then the output will be in ./dist/stego_lsb


## Run Options

usage: stego_lsb [-h] -r RED_BITS -g GREEN_BITS -b BLUE_BITS [-i INPUT_SCHEME] [-o OUTPUT_SCHEME] -f FILE [-m MESSAGE] -p
                 {hide,extract,test}
stego_lsb: error: the following arguments are required: -r/--red-bits, -g/--green-bits, -b/--blue-bits, -f/--file, -p/--operation


