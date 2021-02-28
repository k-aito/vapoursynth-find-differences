#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vapoursynth-find-differences.py
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

"""
Vapoursynth-find-differences.py can be used to find where there are black frames in a video
- Compare each frames to another one
- If the difference is lower than the percent (0.1 by default) we keep the frame in memory
- It display the intervals of all the frames at end
"""

################
# PARSING ARGS #
################

import argparse
parser = argparse.ArgumentParser()

# MANDATORY: -s / --source
parser.add_argument("-s", "--source",
                    required=True,
                    help="Paths of the video")

# OPTIONAL: -d / --diff
parser.add_argument("-d", "--diff",
                    required=False,
                    help="Video that will be used for comparison if they have the same amount of frames (default: black blankclip)")

# OPTIONAL: -p / --percent
parser.add_argument("-p", "--percent",
                    required=False,
                    help="Percent of difference between video and another frames, 0 minimum and 1 maximum (default 0.1), "
                         + "if we compare to another video we display the frames that are different of 0 instead of lower to the percent")

# OPTIONAL: -v / --verbose
parser.add_argument("-v", "--verbose",
                    required=False,
                    help="Enable debug and progression for the frames in intervals (default: disabled)",
                    action='store_true')

# OPTIONAL: -vv / --veryverbose
parser.add_argument("-vv", "--veryverbose",
                    required=False,
                    help="Enable debug and progression while scanning each frames (default: disabled)",
                    action='store_true')

args = parser.parse_args()

###############
# VAPOURSYNTH #
###############

import vapoursynth as vs
core = vs.get_core()

v = core.ffms2.Source(args.source)

sceneFrames = []

if args.diff == None:
  black = core.std.BlankClip(v, keep=1)
  diff = core.std.PlaneStats(v, black)

  # Define args.percent if not defined
  if args.percent == None:
    args.percent = 0.1
else:
  v2 = core.ffms2.Source(args.diff)
  # Check that the amount of frames are the same if not quit
  if v.num_frames == v2.num_frames:
    diff = core.std.PlaneStats(v, v2)
  else:
    print("ERROR: the amount of frames are not the same (v1: {} / v2: {})".format(v.num_frames, v2.num_frames))
    import os
    os._exit(1)

fps = diff.fps.numerator / diff.fps.denominator

print("INFO: Start the comparison of each frames")
for i in range(0, diff.num_frames):
  if args.veryverbose:
    print('{} / {} [PlaneStatsDiff: {}]'.format(i, diff.num_frames, diff.get_frame(i).props['PlaneStatsDiff']))
  else:
    if i % 1000 == 0 and not args.verbose:
      print("PROGRESS: Compare {} on {}".format(i, diff.num_frames))
  if args.diff:
    if diff.get_frame(i).props['PlaneStatsDiff'] != 0.0:
      if args.verbose:
        print('{} / {} [PlaneStatsDiff: {}]'.format(i, diff.num_frames, diff.get_frame(i).props['PlaneStatsDiff']))
      sceneFrames.append(i)
  else:
    if diff.get_frame(i).props['PlaneStatsDiff'] < float(args.percent):
      if args.verbose:
        print('{} / {} [PlaneStatsDiff: {}]'.format(i, diff.num_frames, diff.get_frame(i).props['PlaneStatsDiff']))
      sceneFrames.append(i)
print("")

sceneSlices = []
startSlice = -1
endSlice = -1

# Make slices from list
for i,value in enumerate(sceneFrames):
  # Guess next value
  nextValueGuess = value + 1
  # Define real next value
  try:
    nextValue = sceneFrames[i + 1]
  except IndexError:
    # We are at end of sceneFrames
    nextValue = sceneFrames[i]

  # Set startSlice if -1
  if startSlice == -1:
    startSlice = value

  # Slice processing
  if nextValueGuess == nextValue:
    sliceFlag = True
  else:
    sliceFlag = False
    # Actual value is endSlice
    endSlice = value

    # Method to convert seconds in hh:mm:ss
    # https://bbs.archlinux.org/viewtopic.php?id=77634
    def humanize_time(secs):
      mins, secs = divmod(secs, 60)
      hours, mins = divmod(mins, 60)
      return '%02d:%02d:%02d' % (hours, mins, secs)

    # Convert in time range
    totalStart = int(startSlice/fps)
    timeStart = humanize_time(totalStart)

    # Convert in time range
    totalEnd = int(endSlice/fps)
    timeEnd = humanize_time(totalEnd)

    # Convert the duration
    durationFrames = endSlice - startSlice
    durationTime = totalEnd - totalStart

    # Append the range
    sceneSlices.append("{} - {} [{}s] ({} - {} [{} frames])".format(timeStart, timeEnd, durationTime, startSlice, endSlice, durationFrames))

    # Reset startSlice
    startSlice = -1

print("INFO: Intervals that maybe have differences")
import pprint
pprint.pprint(sceneSlices)
