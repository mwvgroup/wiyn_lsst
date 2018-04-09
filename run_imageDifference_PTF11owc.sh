#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=PTF11owc seq=A filter=H night=20111115 expnum=313 \
    --id field=PTF11owc seq=A filter=H night=20111121 expnum=161 \
    --id field=PTF11owc seq=A filter=H night=20111208 expnum=381 \
    --id field=PTF11owc seq=A filter=H night=20120402 expnum=175 \
    --templateId field=PTF11owc seq=A filter=H night=20121125 expnum=615 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=PTF11owc seq=A filter=J night=20111115 expnum=371 \
    --id field=PTF11owc seq=A filter=J night=20111121 expnum=175 \
    --id field=PTF11owc seq=A filter=J night=20111208 expnum=429 \
    --templateId field=PTF11owc seq=A filter=J night=20120402 expnum=208 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
