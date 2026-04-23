#!python3

import logging

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(message)s",
    datefmt="%Y/%d/%m %H:%M:%S",
)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

import argparse
from collections import OrderedDict


##########################################################################
##
##    オプションを変換する
##

def convert_options(args):

    slopts = OrderedDict()

    return  slopts
# End Def (convert_options)


##########################################################################
##
##    オプションを生成する
##

def generate_slurm_options(args):

    cmd='sbatch '

    if args.project:
        cmd += f"  --partition  {args.project}"
    if args.job_name:
        cmd += f"  --jobname  {args.job_name}"

    print(cmd)
# End Def (generate_slurm_options)


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
        '-m', dest='mail_events',
        type=str, required=False, default=None,
        metavar='mail_events',
    )
    parser.add_argument(
        '-M', dest='mail_list',
        type=str, required=False, default=None,
        metavar='user_list',
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

    parser.add_argument(
        'script',
        type=str,
    )

    return  parser.parse_args()
# End Def (parse_args)


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
