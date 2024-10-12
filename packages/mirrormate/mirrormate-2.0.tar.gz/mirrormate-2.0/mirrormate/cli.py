# mirrormate/cli.py

import argparse
import mirrormate.cloner as cloner

def main():
    parser = argparse.ArgumentParser(description="Clone websites or download specific files using wget.")
    parser.add_argument("--mirror", help="URL of the website to mirror", type=str)
    parser.add_argument("--copy", help="URL of the specific file to download", type=str)
    parser.add_argument("--file", help="File type to download (e.g., .py)", type=str)
    parser.add_argument("--url", help="URL of the website to download specific file types from", type=str)

    args = parser.parse_args()

    if args.mirror:
        print("Starting to mirror the website...")
        if cloner.clone(url=args.mirror, silent=False):
            print(f"Successfully mirrored the website: {args.mirror}")
        else:
            print("Error: Unable to mirror the website or disallowed by robots.txt.")

    elif args.copy:
        print("Starting to download the file...")
        if cloner.clone(file_url=args.copy, silent=False):
            print(f"Successfully downloaded the file: {args.copy}")
        else:
            print("Error: Unable to download the file or disallowed by robots.txt.")

    elif args.file and args.url:
        print(f"Starting to download all '{args.file}' files from the specified URL...")
        if cloner.clone(file_format=args.file, url=args.url, silent=False):
            print(f"Successfully downloaded all '{args.file}' files from: {args.url}")
        else:
            print("Error: Unable to download files or disallowed by robots.txt.")

    else:
        print("Please provide a valid option. Use --mirror, --copy, or --file with --url.")

if __name__ == "__main__":
    main()
