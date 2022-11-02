import argparse
class Arguments:
    def __init__(self):
        self.prog_name = 'wallpaper-gen'
        self.description = 'Creeates a kawaii-waifu wallpaper!'
        self.version = '0.1.0'
        self.arguments = [
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
                    'version' : '{} {}'.format('%(prog)s',self.version),
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
                    'default' : 1000,
                    'help' : 'ornament'
                }),
                (('--ornament_samples'),{
                    'type' : int,
                    'metavar' : 'ORNAMENT_SAMPLES',
                    'default' : 20,
                    'help' : 'ornament'
                }),
                (('--ornament_minimum_distance'),{
                    'type' : int,
                    'metavar' : 'ORNAMENT_MINIMUM_DISTANCE',
                    'default' : 75,
                    'help' : 'ornament'
                })
            ]

    def parser_wrapper(self, parser, args):
        if (type(args[0]) == str):
            parser.add_argument(args[0],**args[1])
        else:
            parser.add_argument(*args[0],**args[1])

    def parser_args(self):
        parser = argparse.ArgumentParser(prog=self.prog_name, description=self.description)
        for args in self.arguments : self.parser_wrapper(parser,args)
        return parser.parse_args()
