#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

# Don't use multiple threads in BLAS, because we're parallelizing at the image level.
export OMP_NUM_THREADS=1

processCcd.py "${REPO}" --rerun processCcd \
    @dr1_dataid.list \
    -j 4 \
    --configfile config/processCcd.py \
    --clobber-versions \
    --clobber-config

#    --loglevel DEBUG \
#    --debug
