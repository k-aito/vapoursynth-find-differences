# vapoursynth-find-differences

## Goal

The goal of this script is to find frames that have differences (defined by the -p argument) to black frames or between 2 videos only if they have the same amount of frames.

- It can be useful for syncing audios or subs because most time desync can happen at these transition.
- It also helps to define segments in the video that can be used for checking the sync.
- The intervals are not always right and desync can happen elsewhere because the video is different or for other unknown reasons.
- With the difference mode it can help to find the frames that are different between 2 videos.

## Requirements

* [Debian](DEBIAN.md)

* [Windows](WINDOWS.md)

## Use

```
usage: vapoursynth-find-differences.py [-h] -s SOURCE [-d DIFF] [-p PERCENT]
                                       [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Paths of the video
  -d DIFF, --diff DIFF  Video that will be used for comparison if they have
                        the same amount of frames (default: black blankclip)
  -p PERCENT, --percent PERCENT
                        Percent of difference between video and another
                        frames, 0 minimum and 1 maximum (default 0.1), if we
                        compare to another video we display the frames that
                        are different of 0 instead of lower to the percent
  -v, --verbose         Enable debug and progression for the frames in
                        intervals (default: disabled)
  -vv, --veryverbose    Enable debug and progression while scanning each
                        frames (default: disabled)
```

## Example

```bash
# Compare to a blankclip (black frames)
vapoursynth-find-differences.py --source video.mkv
# Compare to another video
vapoursynth-find-differences.py --source video.mkv --diff video2.mkv
```

## Credits

* Method to convert seconds in a human timecode (https://bbs.archlinux.org/viewtopic.php?id=77634)
