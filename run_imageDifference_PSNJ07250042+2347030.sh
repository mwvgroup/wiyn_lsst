#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcd:imdiff \
    -j 4 \
    --id field=PSNJ07250042+2347030 seq=A filter=H night=20121028 expnum=542 \
    --templateId field=PSNJ07250042+2347030 seq=A filter=H night=20131213 expnum=440 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcd:imdiff \
    -j 4 \
    --id field=PSNJ07250042+2347030 seq=A filter=H night=20121102 expnum=491 \
    --id field=PSNJ07250042+2347030 seq=A filter=H night=20121122 expnum=573 \
    --id field=PSNJ07250042+2347030 seq=A filter=H night=20121125 expnum=526 \
    --id field=PSNJ07250042+2347030 seq=A filter=H night=20121130 expnum=628 \
    --templateId field=PSNJ07250042+2347030 seq=A filter=H night=20131213 expnum=440 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcd:imdiff \
    -j 4 \
    --id field=PSNJ07250042+2347030 seq=A filter=J night=20121028 expnum=533 \
    --id field=PSNJ07250042+2347030 seq=A filter=J night=20121102 expnum=501 \
    --id field=PSNJ07250042+2347030 seq=A filter=J night=20121122 expnum=582 \
    --id field=PSNJ07250042+2347030 seq=A filter=J night=20121125 expnum=535 \
    --id field=PSNJ07250042+2347030 seq=A filter=J night=20121130 expnum=644 \
    --templateId field=PSNJ07250042+2347030 seq=A filter=J night=20131213 expnum=481 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
