#!/bin/bash

set  -u

##########################################################################
##
##    ジョブを投入したディレクトリとカレントディレクトリ
##

# SLURM ではデフォルトでジョブを投げたディレクトリが
# カレントディレクトリになる。

# PBS では、カレントディレクトリは作業用のディレクトリになる
# ジョブを投入したディレクトリは PBS_O_WORKDIR  に入っている

export  PBS_O_WORKDIR=$(pwd)

# ついでに JOB ID を示す環境変数も設定しておく
export  PBS_JOBID=${SLURM_JOB_ID}


##########################################################################
##
##    PBS_NODEFILE
##

scontrol show hostname ${SLURM_JOB_NODELIST}

# まず作成するノードファイルの名前を決めて
# 環境変数 PBS_NODEFILE にセットしておく
export  PBS_NODEFILE="pbs_nodefile.${PBS_JOBID}"

# 適当なコマンドを実行して結果をノードファイルに書き込む
if [[ "X${SLURM_NTASKS}Y" != 'XY' ]] ; then
    srun -n "${SLURM_NTASKS}" hostname | sort | tee "${PBS_NODEFILE}"
else
    echo "SLURM_NTASKS : undefined"  1>&2
    srun --nodes=${SLURM_NNODES} hostname | sort | tee "${PBS_NODEFILE}"
fi


##########################################################################
##
##    スクリプトを起動
##

# SLURM では、普通に引数を渡せそうなので
# スクリプト名は第１引数から読み出す。
# もし引数がなければ、環境変数 PBSEXEC_SCRIPT を参照する
# それも無ければエラーにする

if [[ $# -ge 1 ]] ; then
    _target_script=$1
    shift  1
else
    _target_script="${PBSEXEC_SCRIPT}"
fi

exec  "${_target_script}"  "$@"

# 上記の exec は呼び出し元プロセスの空間を上書きするので
# 正常に呼び出された後はここには来ない（プロセスが異常終了しても同様）
# ここに来るのは、そもそも起動できなかった場合に限る。
# 例えば、指定したプログラムが存在しないなどの場合である。

echo  "FATAL : Could not launch ${_target_script}"
exit  1
