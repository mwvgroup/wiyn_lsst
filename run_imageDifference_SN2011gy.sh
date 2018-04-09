#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011gy seq=A filter=H night=20111115 expnum=323 \
    --id field=SN2011gy seq=A filter=H night=20111121 expnum=119 \
    --id field=SN2011gy seq=A filter=H night=20111208 expnum=307 \
    --id field=SN2011gy seq=A filter=H night=20120108 expnum=287 \
    --id field=SN2011gy seq=A filter=H night=20120402 expnum=93 \
    --templateId field=SN2011gy seq=A filter=H night=20121028 expnum=457 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011gy seq=A filter=J night=20111115 expnum=342 \
    --id field=SN2011gy seq=A filter=J night=20111121 expnum=137 \
    --templateId field=SN2011gy seq=A filter=J night=20121028 expnum=432 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011gy seq=A filter=J night=20111208 expnum=326 \
    --templateId field=SN2011gy seq=A filter=J night=20121028 expnum=432 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False\
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

