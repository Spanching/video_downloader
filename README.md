# Video Downloader with Python

## How to use

Add lines to list.txt to download a segmented video file. The lines are constructed like this: 

```
filename.ending base.url amount.segments
```

Be aware, that the base_url needs to be formattable at the position where the int for the respective segment is inserted. For example:

```
https://www.example.com/video-segment-{}.ts
```