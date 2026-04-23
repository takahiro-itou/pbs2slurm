#!python3

import argparse


##########################################################################
##
##    引数を解析する
##

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-P', dest='project',
        type=str, required=False, default='',
        metavar='project',
    )
    parser.add_argument(
        '-q', dest='queue',
        type=str, required=False, default='',
        metavar='distination',
    )

    return  parser.parse_args()
# End Def (parse_args)


##########################################################################
##
##    オプションを生成する
##

def generate_slurm_options(args):
    pass
# End Def (generate_slurm_options)


##########################################################################
##
##    エントリポイント
##

def main():
    args = parse_args()
    generate_slurm_options(args)
# End Def (main)


if __name__ == '__main__':
    main()
