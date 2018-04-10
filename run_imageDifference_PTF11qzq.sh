#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=PTF11qzq seq=A filter=H night=20111208 expnum=344 \
    --id field=PTF11qzq seq=A filter=H night=20120108 expnum=324 \
    --templateId field=PTF11qzq seq=A filter=H night=20121007 expnum=408 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=PTF11qzq seq=A filter=J night=20111208 expnum=363 \
    --id field=PTF11qzq seq=A filter=J night=20120108 expnum=352 \
    --templateId field=PTF11qzq seq=A filter=J night=20130925 expnum=475 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
