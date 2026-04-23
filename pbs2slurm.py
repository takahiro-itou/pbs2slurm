#!python3

import argparse


##########################################################################
##
##    引数を解析する
##

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-e', dest='stderr_file',
        type=str, required=False, default=None,
        metavar='path',
    )
    parser.add_argument(
        '-j', dest='join',
        type=str, required=False, default=None,
        choices=[ 'oe', 'eo', 'n' ],
    )
    parser.add_argument(
        '-k', dest='keep',
        type=str, required=False, default=None,
    )
    parser.add_argument(
        '-l', dest='resource_list',
        type=str, required=False, default=None,
        metavar='resource_list',
    )
    parser.add_argument(
        '-N', dest='job_name',
        type=str, required=False, default=None,
        metavar='name',
    )
    parser.add_argument(
        '-o', dest='output',
        type=str, required=False, default=None,
        metavar='path',
    )
    parser.add_argument(
        '-P', dest='project',
        type=str, required=False, default=None,
        metavar='project',
    )
    parser.add_argument(
        '-q', dest='queue',
        type=str, required=False, default=None,
        metavar='distination',
    )
    parser.add_argument(
        '-v', dest='variable_list',
        type=str, required=False, default=None,
        metavar='variable_list',
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
