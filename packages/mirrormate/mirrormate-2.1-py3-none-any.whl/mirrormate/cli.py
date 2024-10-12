# mirrormate/cli.py

import argparse
import mirrormate.clone as clone

def main():
    parser = argparse.ArgumentParser(description="Clone websites or download specific files using wget.")
    parser.add_argument("--mirror", help="URL of the website to mirror", type=str)
    parser.add_argument("--copy", help="URL of the specific file to download (e.g., .sql, .py)", type=str)
    parser.add_argument("--file", help="File type to download (e.g., .py)", type=str)
    parser.add_argument("--url", help="URL of the website to download specific file types from", type=str)

    args = parser.parse_args()

    if args.mirror:
        if clone.clone(url=args.mirror, silent=False):
            print(f"Successfully mirrored the website: {args.mirror}")
        else:
            print("Error: Unable to mirror the website.")

    elif args.copy:
        if clone.clone(file_url=args.copy, silent=False):
            print(f"Successfully downloaded the file: {args.copy}")
        else:
            print("Error: Unable to download the file.")

    elif args.file and args.url:
        if clone.clone(file_format=args.file, url=args.url, silent=False):
            print(f"Successfully downloaded all '{args.file}' files from: {args.url}")
        else:
            print("Error: Unable to download files.")

    else:
        print("Please provide a valid option. Use --mirror, --copy, or --file with --url.")

if __name__ == "__main__":
    main()
