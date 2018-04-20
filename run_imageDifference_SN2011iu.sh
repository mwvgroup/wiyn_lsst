#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcd:imdiff \
    -j 4 \
    --id field=SN2011iu seq=A filter=H night=20111208 expnum=234 \
    --id field=SN2011iu seq=A filter=H night=20120108 expnum=195 \
    --templateId field=SN2011iu seq=A filter=H night=20120925 expnum=259 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcd:imdiff \
    -j 4 \
    --id field=SN2011iu seq=A filter=J night=20111208 expnum=252 \
    --id field=SN2011iu seq=A filter=J night=20120108 expnum=214 \
    --templateId field=SN2011iu seq=A filter=J night=20121001 expnum=241 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

