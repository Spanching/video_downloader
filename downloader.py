
import os
import urllib.request


def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar -
                                          filled_progbar), '[{:>7.2%}]'.format(frac), end='')

def download_fragments(base_url, amount):
    retry_list = []
    failed_list = []

    for i in range(1, amount+1):
        progbar(i, amount, 50)
        try:
            urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'videos/{i:05d}.ts')
        except:
            print(f"Error for fragment {i}")
            retry_list.append(i)

    for i in retry_list:
        try:
            urllib.request.urlretrieve(base_url.format(f'{i:05d}'), f'videos/{i:05d}.ts')
        except:
            print("Some fragments could not be downloaded:")
            print(str(failed_list))
            print("aborting now")
            raise Exception

def merge_fragments(name, ending):
    os.chdir("videos")

    fragments = os.listdir(".")

    f = open("../mylist.txt", "w")
    for frag in fragments:
        f.write(f"file 'videos/{frag}'\n")
    f.close()
    os.chdir("..")
    print("merging fragments")
    os.system(f'cmd /c "ffmpeg -hide_banner -loglevel fatal -f concat -i mylist.txt -c copy {name}"')
    return fragments

def remove_fragments(fragments):
    print("remove fragments")
    os.remove("mylist.txt")
    for frag in fragments:
        os.remove(f"videos/{frag}")

def test_prerequisits():
    fragments = os.listdir("videos")
    if fragments:
        for frag in fragments:
            os.remove(f"videos/{frag}")

with open("list.txt") as f:
    test_prerequisits()
    for line in f.readlines():
        (filename, base_url, amount) = line.split(" ")
        ending = filename.split(".")[-1]
        amount = int(amount)
        print(f"Downloading {filename}")
        download_fragments(base_url, amount)
        fragments = merge_fragments(filename, ending)
        remove_fragments(fragments)
        print(f"Downloading {filename} done")