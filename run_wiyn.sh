#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

export OMP_NUM_THREADS=1

#    @science_ids_dr2.list \
#    --id field='SN2013cb' seq=A filter=H night=20130519\
#    --id field='iPTF13ebh' seq=A filter=H night=20131120\
#    --id field='iPTF13ebh' seq=A filter=H night=20131209\
#    --id field='iPTF13ebh' seq=A filter=H night=20131213\
processCcd.py "${REPO}" --rerun processCcd \
    -j 4 \
    --id field='LSQ13cwp' seq=A filter=H night=20131111 \
    --id field='LSQ13cwp' seq=A filter=H night=20131120 \
    --id field='LSQ13cwp' seq=A filter=H night=20131209 \
    --id field='LSQ13cwp' seq=A filter=H night=20131213 \
    --id field='LSQ13cwp' seq=A filter=J night=20131111 \
    --id field='LSQ13cwp' seq=A filter=J night=20131120 \
    --id field='LSQ13cwp' seq=A filter=J night=20131209 \
    --id field='LSQ13cwp' seq=A filter=J night=20131213 \
    --id field='PTF11mty' seq=A filter=H night=20111025 \
    --id field='PTF11mty' seq=A filter=H night=20111115 \
    --id field='PTF11mty' seq=A filter=H night=20120925 \
    --id field='PTF11mty' seq=A filter=J night=20111025 \
    --id field='PTF11mty' seq=A filter=J night=20111115 \
    --id field='PTF11mty' seq=A filter=J night=20121007 \
    --configfile config/processCcd.py \
    --clobber-versions

#    --loglevel DEBUG \
#    --debug
