import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import argparse
from parser import Parser


def main():
    sysParser = argparse.ArgumentParser(description="Convert text to different formats")
    sysParser.add_argument("--inputPath", required=True ,help="Input text file location")
    sysParser.add_argument("--outputFolderPath",  required=True ,help="Output folder location")

    args = sysParser.parse_args()

    parser: Parser = Parser()

    parser.covert(args.inputPath, args.outputFolderPath)


if __name__ == "__main__":
    main()
