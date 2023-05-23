# Video Fragment Downloader with Python

This is a video downloader, that can download videos that are fragmented into many short video files.

## Prerequisites

You need to have ffmpeg installed and added to your PATH. You can install it [here](https://ffmpeg.org/). It is used to merge the video fragments together as it is much faster than using python for that task.

## Basic usage

Basically the program can do two things, it can download a single fragmented video or multiple videos that are specified in a file. For each video the steps are pretty simple:

1. Remove everything that lies in the temporary folder (default: ```tmp```)
1. Download all fragments for the whole video
1. Merge all the video fragments together using ffmpeg
1. Remove temporary files and folders

### Single Video Download 

#### Easiest Example

If your URL contains the part 'seg-XXX' for each video segment, you can download that video by passing the last segment URL to this program like this:

```python
python -u fragment_downloader single https://example.com/something/seg-97-a1v9.ts/
```

The downloader will then download 97 segments from that URL.

#### Usage

To download a single video, you can use:

```python
python -u fragment_downloader single --name name.ts --amount 12 https://example.com/something/seg-{}-a1v9.ts/
```

In this case, the downloader will download 12 fragments from ```https://example.com/``` and merge them together in the file ```name.ts```.

#### Additional arguments

Arguments are structured like follows:

```
python fragment_downloader [front] single "name" "amount" "base_url" [back]
```

|argument|shortcut|position|description|
|-|-|-|-|
|-remove-existing|-r|front| Specifies if existing files in temporary folder should be removed |
|-path|-p|front| Specifies path for temporary storage of video fragments |
|-output|-o|front| Specifies path for outputting the finished video file |
|-keep-fragments|-k|back| Specifies if video fragments should be kept after merging |



### Multi Video Download

#### Usage

To download multiple videos, you have to specify them in a file, preferrably in the root folder of this project. The file is structured like this:

```
name.ending amount base_url
example.ts 12 https://example.com/something/fragment-{}-a1v9.ts/
```

To download all these videos, use:

```python
python -u fragment_downloader multi your_file.txt
```

#### Additional arguments

Arguments are structured like follows:

```
python fragment_downloader [arg] multi "file"
```

|argument|shortcut|description|
|-|-|-|
|-remove-existing|-r| Specifies if existing files in temporary folder should be removed |
|-path|-p| Specifies path for temporary storage of video fragments |
|-output|-o| Specifies path for outputting the finished video file |