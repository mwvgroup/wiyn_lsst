#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

#    @science_ids_dr2.list \
#    --id field='SN2013cb' seq=A filter=H night=20130519 expnum=210 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131120 expnum=263 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131209 expnum=088 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131213 expnum=137 \
processCcd.py "${REPO}" -rerun processCcdOutputs \
    --id field='LSQ13cwp' seq=A filter=H night=20131111 expnum=521 \
    --id field='LSQ13cwp' seq=A filter=H night=20131120 expnum=335 \
    --id field='LSQ13cwp' seq=A filter=H night=20131209 expnum=312 \
    --id field='LSQ13cwp' seq=A filter=H night=20131213 expnum=274 \
    --id field='LSQ13cwp' seq=A filter=J night=20131111 expnum=562 \
    --id field='LSQ13cwp' seq=A filter=J night=20131120 expnum=425 \
    --id field='LSQ13cwp' seq=A filter=J night=20131209 expnum=335 \
    --id field='LSQ13cwp' seq=A filter=J night=20131213 expnum=299 \
    --id field='PTF11mty' seq=A filter=H night=20111025 expnum=218 \
    --id field='PTF11mty' seq=A filter=H night=20111115 expnum=112 \
    --id field='PTF11mty' seq=A filter=H night=20120925 expnum=81 \
    --id field='PTF11mty' seq=A filter=J night=20111025 expnum=200 \
    --id field='PTF11mty' seq=A filter=J night=20111115 expnum=130 \
    --id field='PTF11mty' seq=A filter=J night=20121007 expnum=50 \
    --configfile config/processCcd.py

#    --loglevel DEBUG \
#    --debug
