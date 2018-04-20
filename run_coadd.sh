#!/bin/bash

REPO=$1
FIELD=$2
TRACT=$3
SEQ=$4
FILTER=$5
NIGHT=$6

PATCH=0,0

COADD_RERUN=coadd
PROCESSCCD_RERUN=processCcd

# The following explicitly iterate between H, J
# for the given FIELD+TRACT.
makeCoaddTempExp.py "${REPO}" --rerun "${COADD_RERUN}" \
    -j 4 \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

makeCoaddTempExp.py "${REPO}" --rerun "${COADD_RERUN}" \
    -j 4 \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

assembleCoadd.py "${REPO}" --rerun "${COADD_RERUN}" \
    -j 4 \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH}

assembleCoadd.py "${REPO}" --rerun "${COADD_RERUN}" \
    -j 4 \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH}
