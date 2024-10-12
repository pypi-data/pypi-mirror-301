import argparse
import sys
from mirrormate import clone

def main():
    parser = argparse.ArgumentParser(
        description="Mirror or download files from websites.",
        epilog="Author: Your Name\nCopyright (c) 2024 Your Name. All rights reserved."
    )
    parser.add_argument('--mirror', help="URL to mirror")
    parser.add_argument('--copy', help="Single file URL to download")
    
    args = parser.parse_args()

    if args.mirror:
        if clone(url=args.mirror, silent=False):
            print("Successfully mirrored the website.")
        else:
            print("Not downloadable.")
    elif args.copy:
        if clone(file_url=args.copy, silent=False):
            print("Successfully downloaded the file.")
        else:
            print("Not downloadable.")
    else:
        print("Please provide valid arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
