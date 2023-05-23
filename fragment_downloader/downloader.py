
import os
import urllib.request
from pathlib import Path

class Downloader:

    def __init__(self, dir, output_dir) -> None:
        self.directory = dir
        self.output_directory = output_dir
        self.ending = 'ts'

    def dowload_and_merge(self, base_url, amount, filename, remove = True, index:int=None):
        self.index = index
        self.__test_prerequisits()
        self.__download_fragments(base_url, amount)
        fragments = self.__merge_fragments(filename)
        if remove:
            self.__remove_fragments(fragments)

    def progbar(self, curr, total, full_progbar):
        frac = curr/total
        filled_progbar = round(frac*full_progbar)
        print('\r', '#'*filled_progbar + '-'*(full_progbar -
                                            filled_progbar), '[{:>7.2%}]'.format(frac), end='')

    def __download_fragments(self, base_url, amount):
        retry_list = []
        for i in range(1, amount+1):
            self.progbar(i, amount, 50)
            try:
                if self.index == None:
                    urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'{self.directory}/{i:05d}.{self.ending}')
                else:
                    urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'{self.directory}{self.index}/{i:05d}.{self.ending}')
            except KeyboardInterrupt:
                print("\nYou typed Ctrl+C. Aborting.")
                raise KeyboardInterrupt
            except:
                print(f"\nError for fragment {i}")
                retry_list.append(i)

        for i in retry_list:
            try:
                urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'{self.directory}/{i:05d}.{self.ending}')
                print(f"\nRetry for fragment {i} successful.")
            except:
                raise Exception(f"Some of these fragments could not be downloaded: {retry_list}, aborting now.")

    def __merge_fragments(self, name):
        os.chdir(f"{self.directory}")

        fragments = os.listdir(".")

        with open("../mylist.txt", "w") as f:
            for frag in fragments:
                f.write(f"file '{self.directory}/{frag}'\n")
        os.chdir("..")
        print("\nmerging fragments")
        os.system(f'cmd /c "ffmpeg -hide_banner -loglevel fatal -f concat -i mylist.txt -c copy {self.output_directory}/{name}"')
        return fragments

    def __remove_fragments(self, fragments):
        print("remove fragments")
        os.remove("mylist.txt")
        for frag in fragments:
            os.remove(f"{self.directory}/{frag}")
        os.removedirs(self.directory)

    def __test_prerequisits(self):
        Path(self.directory).mkdir(parents=True, exist_ok=True)
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        fragments = os.listdir(f"{self.directory}")
        if fragments:
            for frag in fragments:
                os.remove(f"{self.directory}/{frag}")