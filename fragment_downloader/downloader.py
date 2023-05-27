import os
import urllib.request
from pathlib import Path
from urllib.error import ContentTooShortError, URLError
import tqdm

from fragment_downloader.errors import FragmentDownloadException


class Downloader:

    def __init__(self, directory, output_directory, index: int = None) -> None:
        self.index = index
        self.directory = directory
        self.output_directory = output_directory
        self.ending = 'ts'

    def download_and_merge(self, base_url, amount, filename, remove=True):
        self.__test_prerequisites()
        self.__download_fragments(base_url, amount)
        fragments = self.__merge_fragments(filename)
        if remove:
            self.__remove_fragments(fragments)

    def __download_fragments(self, base_url, amount):
        retry_list = []
        for i in tqdm.tqdm(range(1, amount + 1), ncols=100, colour="#00ff00"):
            try:
                urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'{self.directory}/{i:05d}.{self.ending}')
            except (ContentTooShortError, URLError):
                print(f"\nError for fragment {i}, will be retried later.")
                retry_list.append(i)

        for i in retry_list:
            try:
                urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'{self.directory}/{i:05d}.{self.ending}')
                print(f"\nRetry for fragment {i} successful.")
            except (ContentTooShortError, URLError):
                raise FragmentDownloadException(f"Some of these fragments could not be downloaded: {retry_list}, "
                                                f"aborting now.")

    def __merge_fragments(self, name):
        os.chdir(f"{self.directory}")

        fragments = sorted(os.listdir("."))
        file = "../mylist.txt" if self.index is None else f"../mylist{self.index}.txt"
        with open(file, "w") as f:
            for frag in fragments:
                f.write(f"file '{self.directory}/{frag}'\n")
        os.chdir("..")
        os.system(
            f'ffmpeg -hide_banner -loglevel fatal -f concat -i mylist.txt -c copy {self.output_directory}/{name}')
        return fragments

    def __remove_fragments(self, fragments):
        if self.index is None:
            os.remove("mylist.txt")
        else:
            os.remove(f"mylist{self.index}.txt")
        for frag in fragments:
            os.remove(f"{self.directory}/{frag}")
        os.removedirs(self.directory)

    def __test_prerequisites(self):
        Path(self.directory).mkdir(parents=True, exist_ok=True)
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        fragments = os.listdir(f"{self.directory}")
        if fragments:
            for frag in fragments:
                os.remove(f"{self.directory}/{frag}")
