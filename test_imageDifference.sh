#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

imageDifference.py ${REPO} --rerun processCcdOutputs:imdiff \
    --id field=PTF11mty seq=A filter=J night=20111025 expnum=200 \
    --id field=PTF11mty seq=A filter=J night=20111115 expnum=130 \
   --templateId field=PTF11mty seq=A filter=J night=20121007 expnum=50 \
   --configfile config/imageDifference.py \
   --config convolveTemplate=True \
   --clobber-config \
   --clobber-versions
