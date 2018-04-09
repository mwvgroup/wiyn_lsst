#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2012fm seq=A filter=H night=20121028 expnum=493 \
    --id field=SN2012fm seq=A filter=H night=20121102 expnum=536 \
    --id field=SN2012fm seq=A filter=H night=20121122 expnum=624 \
    --id field=SN2012fm seq=A filter=H night=20121130 expnum=660 \
    --templateId field=SN2012fm seq=A filter=H night=20131018 expnum=197 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2012fm seq=A filter=H night=20121125 expnum=481 \
    --templateId field=SN2012fm seq=A filter=H night=20131018 expnum=197 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=SN2012fm seq=A filter=J night=20121028 expnum=484 \
    --id field=SN2012fm seq=A filter=J night=20121102 expnum=546 \
    --id field=SN2012fm seq=A filter=J night=20121122 expnum=633 \
    --id field=SN2012fm seq=A filter=J night=20121125 expnum=490 \
    --id field=SN2012fm seq=A filter=J night=20121130 expnum=669 \
    --templateId field=SN2012fm seq=A filter=J night=20131018 expnum=222 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
