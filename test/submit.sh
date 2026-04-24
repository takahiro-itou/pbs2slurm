#!/bin/bash  -xue

script_file=${BASH_SOURCE:-$0}
script_dir=$(readlink -f "$(dirname "${script_file}")")

export  DEFAULT_NGPUS=8

"${script_dir}/../qsub"  \
    -P GROUP  \
    -q QUEUE_NAME  \
    -o OUTPUT.o  \
    -j oe  \
    -kdoe  \
    -m abe  \
    -M MAIL \
    -l select=16:mpiprocs=8:ompthreads=1  \
    -lwalltime=01:02:03  \
    -v SCRIPT_DIR=${script_dir},TARGET_SCRIPT=sample.sh  \
    -N TEST-JOB-NAME  \
    slurmexec-helper.sh     \
    sample.sh         \
    arg1  arg2        \
    "$@"              \
;
