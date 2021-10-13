import argparse
import os

from pipeline import StegoPipeline
from processors import LSBStegoProcessor
from utils import binary_to_text


def get_cli_args():
    # creates the parser
    parser = argparse.ArgumentParser(description="Run a Stego LSB pipeline")

    # the bits to hide for each color component
    parser.add_argument("-r", "--red-bits", action="store",
                        type=int, required=True,
                        help="bits to hide in first component")
    parser.add_argument("-g", "--green-bits", action="store",
                        type=int, required=True,
                        help="bits to hide in second component")
    parser.add_argument("-b", "--blue-bits", action="store",
                        type=int, required=True,
                        help="bits to hide in third component")

    # the input/output schemes
    parser.add_argument("-i", "--input-scheme", action="store", type=str,
                        default="rgb", help="the input color space")
    parser.add_argument("-o", "--output-scheme", action="store", type=str,
                        default="rgb", help="the output color space")

    # output/input file
    parser.add_argument("-f", "--file", action="store", type=str,
                        required=True, help="the file to process")

    # message
    parser.add_argument("-m", "--message", action="store", type=str,
                        help="the message to hide")

    # operation to perform
    parser.add_argument("-p", "--operation", action="store", type=str,
                        choices=["hide", "extract", "test"], required=True,
                        help="either hides, extracts, or runs hiding and extracting")

    args = parser.parse_args()
    return vars(args)


def main():
    kwargs = get_cli_args()
    lsb_stego_processor = LSBStegoProcessor((kwargs["red_bits"],
                                             kwargs["green_bits"],
                                             kwargs["blue_bits"]),
                                             input_scheme=kwargs["input_scheme"],
                                             output_scheme=kwargs["output_scheme"])

    pipeline = StegoPipeline(kwargs["file"],
                             steps=[("lsb_stego_processor",
                                     lsb_stego_processor)]
                             )

    # runs the operations
    output_path = kwargs["file"]
    if (operation := kwargs["operation"]) == "hide" or operation == "test":
        # processes the operation 
        split_file_path = os.path.split(output_path)
        output_path = os.path.join(split_file_path[0],
                                   "stego_lsb_" + split_file_path[1])
        pipeline.hide(msg=kwargs["message"], file_path=output_path)

    if operation == "extract" or operation == "test":
        msg = pipeline.extract(output_path)
        translated_msg = binary_to_text(msg)
        print(f"Extracted message:\n{translated_msg}")


if __name__ == "__main__":
    main()
