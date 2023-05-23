import argparse
from threading import Thread

from fragment_downloader.downloader import *
from datetime import datetime

from fragment_downloader.errors import InvalidUrlException

endings = [".ts", ".mp4", ".avi", ".mkv", ".mov", ".wmv"]


def run():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    parser.add_argument('-p', '--path', type=str,
                        help='Path to the temporary folder where the video fragments will be stored', default='tmp')
    parser.add_argument('-o', '--output-path', type=str, help='The path to output the video in', default='output')

    single = subparser.add_parser("single")
    single.add_argument('base_url', type=str, help="Base URL of the fragments to download")
    single.add_argument('-n', '--name', type=str, help="Name of the output file")
    single.add_argument('-a', '--amount', type=int, help="Specify the amount of fragments manually")
    single.add_argument('-k', '--keep-fragments', action='store_true',
                        help="If specified, fragments will not be removed from the folder")

    multi = subparser.add_parser("multi")
    multi.add_argument('file', type=str, help="Name of the file used for multiple downloads after each other")

    args = parser.parse_args()

    if args.command == "single":
        validate_arguments(args)
        if args.name is None:
            filename = get_default_file_name()
        else:
            filename = args.name
        base_url = args.base_url
        if args.amount is None:
            amount, base_url = amount_url_from_url(base_url)
        else:
            amount = args.amount
        keep = args.keep_fragments
        downloader = Downloader(args.path, args.output_path)
        downloader.download_and_merge(base_url, amount, filename, not keep)
    elif args.command == "multi":
        input_file = args.file
        with open(input_file) as f:
            for index, line in enumerate(f.readlines()):
                downloader = Downloader(f"{args.path}{index}", args.output_path, index)
                if len(line.split(" ")) == 3:
                    filename, amount, base_url = line.split(" ")
                    base_url = base_url.strip(' "\'\n')
                    amount = int(amount)
                elif len(line.split(" ")) == 2:
                    arg, base_url = line.split(" ")
                    base_url = base_url.strip(' "\'\n')
                    try:
                        int(arg)
                    except ValueError:
                        filename = arg
                        amount, base_url = amount_url_from_url(base_url)
                    else:
                        amount = int(arg)
                        filename = get_default_file_name(index)
                elif len(line.split(" ")) == 1:
                    base_url = line
                    base_url = base_url.strip(' "\'\n')
                    amount, base_url = amount_url_from_url(base_url)
                    filename = get_default_file_name(index)
                Thread(target=downloader.download_and_merge, args=(base_url, amount, filename)).start()


def validate_arguments(args):
    if args.amount is None:
        if "{}" in args.base_url:
            raise InvalidUrlException("No amount specified but found placeholder '{}' in url")
        if "seg-" not in args.base_url:
            raise InvalidUrlException(
                "Could not find 'seg-' in the url, please specify a url with placeholder and the amount manually")
    else:
        if "{}" not in args.base_url:
            raise InvalidUrlException("An amount was specified, but there is no placeholder in the url")
    if args.name is not None:
        for ending in endings:
            if args.name.endswith(ending):
                break
        else:
            args.name = f"{args.name}.mp4"


def amount_url_from_url(url: str) -> tuple:
    amount = int(url.split("seg-")[1].split("-")[0])
    url = url.replace(f"seg-{amount}", "seg-{}")
    return amount, url


def get_default_file_name(index: int = None):
    date_time = datetime.fromtimestamp(datetime.now().timestamp())
    str_date_time = date_time.strftime("%Y%m%d%H%M%S")
    if index is None:
        return f"Downloaded_content_{str_date_time}.mp4"
    else:
        return f"Downloaded_content_{str_date_time}_{index}.mp4"
