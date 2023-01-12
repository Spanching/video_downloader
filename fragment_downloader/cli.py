import argparse
from downloader import *

def run():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    parser.add_argument('-r', '--remove-existing', action='store_true', help="If specified, anything in the temporary folder will be removed before starting the download")
    parser.add_argument('-p', '--path', type=str, help='Path to the temporary folder where the video fragments will be stored', default='tmp')
    parser.add_argument('-o', '--output-path', type=str, help='The path to output the video in', default='output')
    single = subparser.add_parser("single")

    single.add_argument('name', type=str, help="Name of the output file")
    single.add_argument("amount", type=int, help="How many fragments there are")
    single.add_argument('base_url', type=str, help="Formattable base URL of the fragments to download")
    single.add_argument('-k', '--keep-fragments', action='store_true', help="If specified, fragments will not be removed from the folder")

    multi = subparser.add_parser("multi")
    multi.add_argument('file', type=str, help="Name of the file used for multiple downloads after each other")
    args = parser.parse_args()

    downloader = Downloader(args.path, args.output_path)

    if args.command == "single":
        filename = args.name
        base_url = args.base_url
        amount = args.amount
        keep = args.keep_fragments
        downloader.dowload_and_merge(base_url, amount, filename, not keep)
    elif args.command == "multi":
        input_file = args.file
        with open(input_file) as f:
            for line in f.readlines():
                (filename, amount, base_url) = line.split(" ")
                downloader.ending = filename.split('.')[-1]
                amount = int(amount)
                base_url = base_url.strip(" \"'")
                downloader.dowload_and_merge(base_url, amount, filename)