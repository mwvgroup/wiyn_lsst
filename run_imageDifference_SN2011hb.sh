#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011hb seq=A filter=H night=20111115 expnum=197 \
    --id field=SN2011hb seq=A filter=H night=20111208 expnum=196 \
    --templateId field=SN2011hb seq=A filter=H night=20131020 expnum=239 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011hb seq=A filter=H night=20120108 expnum=158 \
    --templateId field=SN2011hb seq=A filter=H night=20131020 expnum=239 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011hb seq=A filter=J night=20111115 expnum=215 \
    --id field=SN2011hb seq=A filter=J night=20111208 expnum=214 \
    --templateId field=SN2011hb seq=A filter=J night=20131020 expnum=289 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2011hb seq=A filter=J night=20120108 expnum=177 \
    --templateId field=SN2011hb seq=A filter=J night=20131020 expnum=289 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=False \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
