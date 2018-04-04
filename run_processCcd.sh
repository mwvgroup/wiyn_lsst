#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

#    @science_ids_dr2.list \
#    --id field='SN2013cb' seq=A filter=H night=20130519 expnum=210 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131120 expnum=263 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131209 expnum=088 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131213 expnum=137 \
processCcd.py "${REPO}" --rerun processCcdOutputs \
    @dr1_dataid.list \
    -j 8 \
    --configfile config/processCcd.py

#    --loglevel DEBUG \
#    --debug
