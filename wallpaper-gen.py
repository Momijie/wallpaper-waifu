'''
     ▄█     █▄     ▄████████  ▄█        ▄█
    ███     ███   ███    ███ ███       ███
    ███     ███   ███    ███ ███       ███
    ███     ███   ███    ███ ███       ███
    ███     ███ ▀███████████ ███       ███
    ███     ███   ███    ███ ███       ███
    ███ ▄█▄ ███   ███    ███ ███▌    ▄ ███▌    ▄
     ▀███▀███▀    ███    █▀  █████▄▄██ █████▄▄██
                             ▀         ▀
       ▄███████▄    ▄████████    ▄███████▄    ▄████████    ▄████████
      ███    ███   ███    ███   ███    ███   ███    ███   ███    ███
      ███    ███   ███    ███   ███    ███   ███    █▀    ███    ███
      ███    ███   ███    ███   ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀
    ▀█████████▀  ▀███████████ ▀█████████▀  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀
      ███          ███    ███   ███          ███    █▄  ▀███████████
      ███          ███    ███   ███          ███    ███   ███    ███
     ▄████▀        ███    █▀   ▄████▀        ██████████   ███    ███
                                                          ███    ███
     ▄█     █▄     ▄████████  ▄█     ▄████████ ███    █▄
    ███     ███   ███    ███ ███    ███    ███ ███    ███
    ███     ███   ███    ███ ███▌   ███    █▀  ███    ███
    ███     ███   ███    ███ ███▌  ▄███▄▄▄     ███    ███
    ███     ███ ▀███████████ ███▌ ▀▀███▀▀▀     ███    ███
    ███     ███   ███    ███ ███    ███        ███    ███
    ███ ▄█▄ ███   ███    ███ ███    ███        ███    ███
     ▀███▀███▀    ███    █▀  █▀     ███        ████████▀
'''

import math
import os
import sys, subprocess
import random
import arguments

from PIL import Image, ImageDraw, ImageColor, ImageOps

def rotate_image(angle, image):
    return image.rotate(angle, expand=True)

def mirror_image(image):
    return ImageOps.mirror(image)

# Just a simple distance formula for 2d points
def distance(point1, point2):
    part1 = (point1[0] - point2[0])**2
    part2 = (point1[1] - point2[1])**2

    return math.sqrt(part1 + part2)

def points_generation(
        total_ornaments,
        sample_size,
        width,height,
        minimum_distance = -1,
        debug=None):
        
    points = []

    # Loop through the total number of ornaments
    # we want to create on the wallpaper
    for i in range(total_ornaments):
        samples = get_random(sample_size, width, height)

        if not points or minimum_distance == -1:
            points.append(samples[0])
        else:
            hold = point_sample_comparison(points, samples, minimum_distance)
            if len(hold) > 0:
                points.append(hold[0])
         
    return points

def point_sample_comparison(points,samples,minimum_distance):
    rtrn = []
    sample_it = 0
    for point in points:
        for sample in samples:
            if distance(point,sample) < minimum_distance:
                del samples[sample_it]
            sample_it += 1
        sample_it = 0
    rtrn = samples

    return rtrn

# get a list (or singular point) of random points
# on a rectangle of defined width and height
def get_random(sample_size, width, height):

    result = (lambda x, width, height :
        [(
            int(random.random() * width),
            int(random.random() * height))
            for i in range(x)
        ])(sample_size, width, height)

    return (result[0][0], result[0][1]) if (len(result) <=1) else result

def add_ornament(args, image):
    ornament = Image.open(args.ornament, 'r')
    ornament.convert('RGBA')

    points = points_generation(args.ornament_num,
            args.ornament_samples,
            args.rect[0],
            args.rect[1],
            args.ornament_minimum_distance,
            args.debug)

    ornament_width, ornament_height = ornament.size
    
    for point in points:
        image.paste(ornament, point, ornament)
        

def add_waifu(args, image):
    waifu = Image.open(args.waifu, 'r')
    waifu = waifu.convert('RGBA')
    waifu = rotate_image(args.angle, waifu)

    if(args.flip):
        waifu = mirror_image(waifu)

    image_width, image_height = image.size
    waifu_width, waifu_height = waifu.size

    x_offset, y_offset = args.offset

    if(args.position == 'top-left'):
        offset = ((0+x_offset), (0+y_offset))
    elif(args.position == 'bottom-left'):
        offset = ((0+x_offset), ((image_height-waifu_height)+y_offset))
    elif(args.position == 'top-right'):
        offset = (((image_width-waifu_width)+x_offset), (0+y_offset))
    elif(args.position == 'bottom-right'):
        offset = (((image_width-waifu_width)+x_offset),
                 ((image_height-waifu_height)+y_offset))
    elif(args.position == 'top-center'):
        x_portion = (int(image_width/2) - int(waifu_width/2))
        offset = ((x_portion+x_offset), (0+y_offset))
    elif(args.position == 'center'):
        x_portion = (int(image_width/2) - int(waifu_width/2))
        y_portion = (int(image_height/2) - int(waifu_height/2))
        offset = ((x_portion+x_offset), (y_portion+y_offset))
    elif(args.position == 'bottom-center'):
        x_portion = (int(image_width/2) - int(waifu_width/2))
        offset = ((x_portion+x_offset),
                 ((image_height-waifu_height)+y_offset))

    image.paste(waifu, offset, waifu)

def base(width, height, color):
    return Image.new('RGBA', (width, height), color=ImageColor.getrgb(color))

def save(image, filename):
    image.save(filename)

def show(args, filename):
    if(args.show):
        imageViewerCmd = {'linux':'xdg-open',
                          'win32':'explorer',
                          'darwin':'open'}[sys.platform]

        subprocess.Popen([imageViewerCmd, filename])

def create_wallpaper(args, width, height, color, filename):
    image = base(width, height, color)
    add_ornament(args, image)
    add_waifu(args, image)
    save(image, filename)

    show(args, filename)
def main() -> int:
    args = arguments.Arguments().parser_args()
    if(args.debug):
        print(args)
    create_wallpaper(args, args.rect[0], args.rect[1], args.color, args.filename)

if __name__ == '__main__':
    raise SystemExit(main())
