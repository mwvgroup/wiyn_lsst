#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

export OMP_NUM_THREADS=1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=LSQ12fuk seq=A filter=H night=20121102 expnum=386 \
    --id field=LSQ12fuk seq=A filter=H night=20121122 expnum=467 \
    --id field=LSQ12fuk seq=A filter=H night=20121125 expnum=424 \
    --id field=LSQ12fuk seq=A filter=H night=20121130 expnum=498 \
    --templateId field=LSQ12fuk seq=A filter=H night=20131019 expnum=224 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    -j 4 \
    --id field=LSQ12fuk seq=A filter=J night=20121102 expnum=396 \
    --id field=LSQ12fuk seq=A filter=J night=20121122 expnum=483 \
    --id field=LSQ12fuk seq=A filter=J night=20121125 expnum=433 \
    --id field=LSQ12fuk seq=A filter=J night=20121130 expnum=505 \
    --templateId field=LSQ12fuk seq=A filter=J night=20131019 expnum=274 \
    --configfile config/imageDifference.py \
    --config convolveTemplate=True \
    --clobber-config \
    --clobber-versions \
    --loglevel ip.diffim=DEBUG
