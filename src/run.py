import os
import sys

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import argparse
from parser import Parser


def main():
    sysParser = argparse.ArgumentParser(description="Convert filtering rules to manifest version 3 rules")
    sysParser.add_argument("--inputPath", type=str, required=True, help="Input text file location")
    sysParser.add_argument("--outputFolderPath", type=str, required=True, help="Output folder location")
    sysParser.add_argument("--maxLength", type=int, default=3000, help="Maximum amount of Rules to be generated")

    args = sysParser.parse_args()

    parser: Parser = Parser()

    parser.convert(args.inputPath, args.outputFolderPath, args.maxLength)


if __name__ == "__main__":
    main()
