# Video Fragment Downloader with Python

This is a video downloader, that can download videos that are fragmented into many short video files.

## Prerequisites

You need to have ffmpeg installed and added to your PATH. You can install it [here](https://ffmpeg.org/). It is used to merge the video fragments together as it is much faster than using python for that task.

## Basic usage

Basically the program can do two things, it can download a single fragmented video or multiple videos that are specified in a file. For each video the steps are pretty simple:

1. Download all fragments for the whole video
1. Merge all the video fragments together using ffmpeg
1. Remove temporary files and folders

### Single Video Download 

#### Easy single Video Download

If your URL contains the part 'seg-XXX' for each video segment, you can download that video by passing the last segment URL to this program like this:

```python
python -u fragment_downloader single "https://example.com/something/seg-97-a1v9.ts/"
```

The downloader will then download 97 segments from that URL into the ```tmp``` folder, merge the fragments into one file stored in the ```output``` directory and remove the fragments and the ```tmp``` folder.

#### Default Usage

To download a single video, you can use:

```python
python -u fragment_downloader single "https://example.com/something/seg-{}-a1v9.ts/" --name name.ts --amount 97
```

In this case, the downloader will download 12 fragments from ```https://example.com/``` and merge them together in the file ```name.ts```.

#### Additional arguments

Arguments are structured like follows:

```
python fragment_downloader [front] single "base_url" [back]
```

|argument|shortcut|position|description|
|-|-|-|-|
|--name|-n|back| The name for the output file, valid file endings for now are ".ts", ".mp4", ".avi", ".mkv", ".mov" and ".wmv". If not provided, defaults to ".mp4"|
|--amount|-a|back| Manually giving the amount of segments, this is only valid for a base_url with '{}' as a placeholder |
|--path|-p|front| Specifies path for temporary storage of video fragments, defaults to 'tmp' |
|--output|-o|front| Specifies path for outputting the finished video file, defaults to 'output' |
|--keep-fragments|-k|back| Specifies if video fragments should be kept after merging defaults to false |



### Multi Video Download

#### Usage

To download multiple videos, you have to specify them in a file, preferably in the root folder of this project. The file can be structured in different ways, the values in parentheses are optional

```
[name[.ending]] [amount] base_url
```

You can also vary the structure in a single file, valid examples are:

```
example.mp4 97 "https://example.com/something/fragment-{}-a1v9.ts/"
example 97 "https://example.com/something/fragment-{}-a1v9.ts/"
97 "https://example.com/something/fragment-{}-a1v9.ts/"
example "https://example.com/something/fragment-97-a1v9.ts/"
"https://example.com/something/fragment-97-a1v9.ts/"
```

Just make sure the name of the files are different if you specify them, otherwise you will be asked if you want to overwrite the existing file.

To download all the videos specified in your file, use:

```python
python -u fragment_downloader multi list.txt
```

#### Additional arguments

Arguments are structured like follows:

```
python fragment_downloader [arg] multi "file"
```

|argument|shortcut|description|
|-|-|-|
|--path|-p|front| Specifies path for temporary storage of video fragments, defaults to 'tmp' |
|--output|-o|front| Specifies path for outputting the finished video file, defaults to 'output' |