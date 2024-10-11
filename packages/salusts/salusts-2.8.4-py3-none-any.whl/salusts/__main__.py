#! /usr/bin/env python3

import sys

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
