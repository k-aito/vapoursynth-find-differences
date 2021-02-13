# vapoursynth-find-black-transition

## Goal

The goal of this script is to find frames that have a lower difference (defined by the -p argument) to black frames.

- It can be useful for syncing audios or subs because most time desync can happen at these transition.
- It also helps to define segments in the video that can be used for checking the sync
- The intervals are not always right and desync can happen elsewhere because the video is different or for other unknown reasons.

## Requirements

* [Debian](DEBIAN.md)

* [Windows](WINDOWS.md)

## Use

```
usage: vapoursynth-find-black-transition.py [-h] -s SOURCE [-p PERCENT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Paths of the video
  -p PERCENT, --percent PERCENT
                        Percent of differnce between video and black frames, 0
                        minimum and 1 maximum (default 0.1)
  -v, --verbose         Enable the progression while scanning each frames
                        (default: disabled)
```

## Example

```bash
vapoursynth-find-black-transition.py --source video.mkv
```

## Credits

* Method to convert seconds in a human timecode (https://bbs.archlinux.org/viewtopic.php?id=77634)
