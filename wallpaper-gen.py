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

import argparse
import math
import os
import sys, subprocess
import random
from PIL import Image, ImageDraw, ImageColor, ImageOps

prog_name = 'wallpaper-gen'
description = 'Creeates a kawaii-waifu wallpaper!'
version = '0.1.0'
arguments = [
        (('filename'), {
            'type' : str,
            'help' : 'filename of wallpaper'
        }),
        (('-r', '--rect'), {
            'type' : str,
            'nargs' : 2,
            'metavar' : ('WIDTH', 'HEIGHT'),
            'default' : [1920,1080],
            'help' : 'set width and height of wallpaper'
        }),
        (('-c', '--color'), {
            'type' : str,
            'default' : '#1E1E2E',
            'help' : 'set color of wallpaper background'
        }),
        (('-waifu', '--waifu'), {
            'type' : str,
            'metavar' : 'PATH',
            'default' : './.default/satori.png',
            'help' : 'path of waifu'
        }),
        (('-p', '--position'), {
            'type' : str,
            'metavar' : 'POS',
            'default' : 'bottom-right',
            'help' : 'Position of waifu'
        }),
        (('-o', '--offset'), {
            'type' : int,
            'nargs' : 2,
            'metavar' : ('X', 'Y'),
            'default' : [0,0],
            'help' :'set offset of waifu'
        }),
        (('-a', '--angle'), {
            'type' : int,
            'metavar' : 'ANGLE',
            'default' : 0,
            'help' : 'The angle the waifu should be rotated by'
        }),
        (('-v', '--version'), {
            'action' : 'version',
            'version' : '{} {}'.format('%(prog)s',version),
            'help' : 'show version number of %(prog)s'
        }),
        (('-d','--debug'), {
            'action' : 'store_true',
            'help' : 'show debug information of %(prog)s'
        }),
        (('-f','--flip'), {
            'action' : 'store_true',
            'help' : 'flips waifu image'
        }),
        (('-s', '--show'), {
            'action' : 'store_true',
            'help' : 'show the wallpaper after it\'s created'
        }),
        (('--ornament'),{
            'type' : str,
            'metavar' : 'ORNAMENT',
            'default' : './.default/star.png',
            'help' : 'ornament'
        }),
         (('--ornament_num'),{
            'type' : int,
            'metavar' : 'ORNAMENT_NUM',
            'default' : 500,
            'help' : 'ornament'
        }),
         (('--ornament_samples'),{
            'type' : int,
            'metavar' : 'ORNAMENT_SAMPLES',
            'default' : 5,
            'help' : 'ornament'
        }),
         (('--ornament_minimum_distance'),{
            'type' : int,
            'metavar' : 'ORNAMENT_MINIMUM_DISTANCE',
            'default' : 100,
            'help' : 'ornament'
        })
    ]

def parser_wrapper(parser, args):
    if (type(args[0]) == str):
        parser.add_argument(args[0],**args[1])
    else:
        parser.add_argument(*args[0],**args[1])

def parser_args():
    parser = argparse.ArgumentParser(prog=prog_name, description=description)

    for args in arguments : parser_wrapper(parser,args)

    return parser.parse_args()

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
    args = parser_args()
    if(args.debug):
        print(args)
    create_wallpaper(args, args.rect[0], args.rect[1], args.color, args.filename)

if __name__ == '__main__':
    raise SystemExit(main())
