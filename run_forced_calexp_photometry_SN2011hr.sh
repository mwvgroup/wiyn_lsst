#!/bin/bash

# Performanced forced-position photometry on all stacks covered by
# the tract of a given coadd

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

FIELD="SN2011hr"
TRACT=`grep ${FIELD} dr1_field_tract.list | cut -f 2 -d ' '`

COADD_RERUN=coaddPhot
FORCEDPHOT_RERUN=forcedPhot

forcedPhotCcd.py "${REPO}" --rerun ${COADD_RERUN}:${FORCEDPHOT_RERUN} \
    --id field=${FIELD} seq=A filter=H night=20111121 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20111208 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20120108 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20120402 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20131213 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20111121 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20111208 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20120108 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20120402 tract=${TRACT} \
    --clobber-versions
