#!/bin/bash

# Performanced forced-position photometry on all stacks covered by
# the tract of a given coadd

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

FIELD="PSNJ07250042+2347030"
TRACT=`grep ${FIELD} dr1_field_tract.list | cut -f 2 -d ' '`

COADD_RERUN=coaddPhot
FORCEDPHOT_RERUN=forcedPhot

forcedPhotCcd.py "${REPO}" --rerun ${COADD_RERUN}:${FORCEDPHOT_RERUN} \
    --id field=${FIELD} seq=A filter=H night=20121028 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20121102 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20121122 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20121125 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20121130 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=H night=20131213 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20121028 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20121102 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20121122 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20121130 tract=${TRACT} \
    --id field=${FIELD} seq=A filter=J night=20131213 tract=${TRACT} \
    --clobber-versions
