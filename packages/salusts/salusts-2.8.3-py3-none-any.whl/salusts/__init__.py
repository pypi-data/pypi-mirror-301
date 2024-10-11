#! /usr/bin/env python3

import sys

__author__ = "HU Xuesong"
__email__ = "galaxy001@gmail.com"

FOVStepX = 429.6
FOVStepY = 709.8
FOVResolution = 3.45/14000 # 0.24642 um/px
DualZoneSides = 8.4  # 34087 px
SoloZoneSides = 11.2 # 45450 px
HEResolution = 0.87/1000 # 0.87 um/px, 3.53x

if __package__ is None:
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from nfo import ChipZoneEdges
else:
    from .nfo import ChipZoneEdges

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print(f"Args:{args}")
    edges = ChipZoneEdges()
    print("Chip Zone Edges:")
    for zone_id, coordinates in edges.items():
        print(f"{zone_id}: {coordinates}")
    return None

if __name__ == "__main__":
    sys.exit(main())
