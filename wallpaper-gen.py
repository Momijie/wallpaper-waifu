"""
Generate a Waifu on a wallpaper!

Copyright (C) 2023 Momijie

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
import sys, subprocess
import random
import arguments

from PIL import Image, ImageColor, ImageOps
from argparse import Namespace

# Just a simple distance formula for 2d points
def distance(
    point1: tuple[int, int], 
    point2: tuple[int, int]
    ) -> float:

    part1 = (point1[0] - point2[0])**2
    part2 = (point1[1] - point2[1])**2

    return math.sqrt(part1 + part2)

def points_generation(
    total_ornaments: int,
    sample_size: int,
    width: int, height: int,
    minimum_distance: int = -1,
    ) -> list:
        
    points = []

    # Loop through the total number of ornaments
    # we want to create on the wallpaper
    for _ in range(total_ornaments):
        samples = get_random(sample_size, width, height)

        if not points or minimum_distance == -1:
            points.append(samples[0])

        else:
            hold = point_sample_comparison(
                points, 
                samples, 
                minimum_distance
            )

            if len(hold) > 0:
                points.append(hold[0])
         
    return points

def point_sample_comparison(
    points: list,
    samples: list | tuple,
    minimum_distance: int
    ) -> list:

    return [
        sample
        for sample in samples 
        if all([
            distance(point, sample) >= minimum_distance 
            for point in points
        ])
    ]
        
# get a list (or singular point) of random points
# on a rectangle of defined width and height
def get_random(
    sample_size: int, 
    width: int, 
    height: int
    ) -> tuple | list[tuple]:

    result = [
        (int(random.random() * width), int(random.random() * height))
        for _ in range(sample_size)
    ]

    return (result[0][0], result[0][1]) if (len(result) <=1) else result

def add_ornament(
    args: Namespace, 
    image: Image.Image
    ) -> None:

    ornament = Image.open(args.ornament, "r")
    ornament.convert("RGBA")

    points = points_generation(
        args.ornament_num,
        args.ornament_samples,
        args.rect[0], args.rect[1],
        args.ornament_minimum_distance
    )
    
    for point in points:
        image.paste(ornament, point, ornament)
    
    ornament.close()

def add_waifu(
    args: Namespace, 
    image: Image.Image
    ) -> None:

    waifu = Image.open(args.waifu, "r")
    waifu = waifu.convert("RGBA")
    waifu = waifu.rotate(args.angle, expand=True)

    if args.flip:
        waifu = ImageOps.mirror(waifu)

    image_width, image_height = image.size
    waifu_width, waifu_height = waifu.size

    x_offset, y_offset = args.offset

    if args.position == "top-left":
        offset = ((0 + x_offset), (0 + y_offset))

    elif args.position == "bottom-left":
        offset = ((0 + x_offset), ((image_height - waifu_height) + y_offset))

    elif args.position == "top-right":
        offset = (((image_width - waifu_width) + x_offset), (0 + y_offset))

    elif args.position == "bottom-right":
        offset = (((image_width - waifu_width) + x_offset),
                 ((image_height - waifu_height) + y_offset))

    elif args.position == "top-center":
        x_portion = (int(image_width/2) - int(waifu_width/2))
        offset = ((x_portion + x_offset), (0 + y_offset))

    elif args.position == "center":
        x_portion = (int(image_width/2) - int(waifu_width/2))
        y_portion = (int(image_height/2) - int(waifu_height/2))
        offset = ((x_portion + x_offset), (y_portion + y_offset))

    elif args.position == "bottom-center":
        x_portion = (int(image_width/2) - int(waifu_width/2))
        offset = ((x_portion + x_offset),
                 ((image_height - waifu_height) + y_offset))
    
    else:
        raise SystemError("Invalid position")

    image.paste(waifu, offset, waifu)
    waifu.close()

def show(
    args: Namespace, 
    filename: str
    ) -> None:

    if not args.show:
        return

    imageViewerCmd = {
        "linux": "xdg-open",
        "win32": "explorer",
        "darwin": "open"
    }.get(sys.platform)
    
    if not imageViewerCmd:
        raise SystemExit("Couldn't get your platform, exiting")

    subprocess.Popen(
        [imageViewerCmd, filename]
    )

def create_wallpaper(
    args: Namespace, 
    width: int, 
    height: int, 
    color: str, 
    filename: str
    ) -> None:

    image = Image.new(
        mode="RGBA", 
        size=(width, height), 
        color=ImageColor.getrgb(color)
    )

    add_ornament(args, image)
    add_waifu(args, image)

    image.save(filename)

    show(args, filename)

def main():
    args = arguments.Arguments().parser_args()

    if args.debug:
        print(args)
    
    if not args.filename.endswith(".png"):
        raise SystemError("Filename must end with '.png'")

    create_wallpaper(
        args, 
        args.rect[0], args.rect[1], 
        args.color, 
        args.filename
    )

if __name__ == "__main__":
    raise SystemExit(main())
