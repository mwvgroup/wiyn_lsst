#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

# Don't use multiple threads in BLAS, because we're parallelizing at the image level.
export OMP_NUM_THREADS=1

processCcd.py "${REPO}" --rerun processCcdOutputs \
    @dr1_dataid.list \
    -j 8 \
    --configfile config/processCcd.py

#    --loglevel DEBUG \
#    --debug
