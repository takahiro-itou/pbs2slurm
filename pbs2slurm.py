#!python3

import logging

logging.basicConfig(
)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

import argparse
import os
from collections import OrderedDict


##########################################################################
##
##    オプションを変換する
##

def convert_options(args):

    _logger.debug(f"{args=}")

    slopts = OrderedDict()
    res = parse_resource_list(args.resource_list)

    # -P (project) は使わないので無視

    # -q (queue) -> --partition
    if args.queue:
        slopts['--partition'] = args.queue

    # - l select ->
    # [NODES] => --nodes,
    # [mpiprocs] => --ntasks-per-node
    # [ngpus] => --gpus-per-node
    sel_nodes = get_resource(res, args, 'nodes', 1)
    slopts['--nodes'] = sel_nodes

    sel_mpiprocs = get_resource(res, args, 'mpiprocs', 1)
    slopts['--ntasks-per-node'] = sel_mpiprocs

    sel_ngpus = get_resource(res, args, 'ngpus', 0, 'DEFAULT_NGPUS')
    if sel_ngpus:
        slopts['--gpus-per-node'] = sel_ngpus

    # -l walltime -> --time
    walltime = res.get('walltime', None)
    if walltime:
        slopts['--time'] = walltime

    # -v --> --export
    if args.variable_list:
        slopts['--export'] = args.variable_list

    # -N --> --job-name
    if args.job_name:
        slopts['--job-name'] = args.job_name

    # -m, -M : メール関係は今回は諦める

    # -j はデフォルトでその動作なので捨てる
    # -k はよくわからないのが多分捨ててよい。

    # -o --> --output
    if args.output:
        slopts['--output'] = args.output

    return  slopts
# End Def (convert_options)


##########################################################################
##
##    オプションを生成する
##

def generate_slurm_options(args):

    slopts = convert_options(args)

    cmd='sbatch '
    for key, val in slopts.items():
        cmd += f"    {key}  {val}"
    # Next (key, val)

    # 起動スクリプト
    cmd += f"  {args.script}  "
    cmd += ' '.join(args.program_args)

    print(cmd)
# End Def (generate_slurm_options)


##########################################################################
##
##    リソースの値を取り出す。
##

def  get_resource(res, args, name, value_default, env_key=None):

    if env_key is not None:
        dvalue = os.environ.get(env_key, value_default)
    else:
        dvalue = value_default
    # End If

    return  res.get(name, dvalue)
# End Def (get_resource)


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
        action='append',
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
    parser.add_argument(
        'program_args',
        type=str, nargs=argparse.REMAINDER,
    )

    return  parser.parse_args()
# End Def (parse_args)


##########################################################################
##
##    リソースリストを解析する。
##

def parse_resource_list(reslist):

    result = {}

    for res in reslist:
        _logger.debug(f"{res=}")
        lhs, rhs = res.split('=', maxsplit=1)
        _logger.debug(f"{lhs=}, {rhs=}")

        if lhs != 'select':
            # select 以外はそのまま突っ込む
            result[lhs] = rhs
            continue
        # End If

        parts = rhs.split(':')
        parts_iter = iter(parts)

        # 最初の要素は、数値の可能性がある
        nodes = 1
        try:
            nodes = int(parts[0])
            next(parts_iter)
        except ValueError:
            # 変換できないのでノード数の指定が省略された形
            nodes = 1
        # End Try

        for r in parts_iter:
            _logger.debug(f"{r=}")
            key, val = r.split('=', maxsplit=1)
            result[key] = val
        # Next (r)

        result['nodes'] = nodes
    # Next (res)

    return  result
# End Def (parse_resource_list)


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
