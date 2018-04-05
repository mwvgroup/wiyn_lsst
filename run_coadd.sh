#!/bin/bash

REPO=$1
FIELD=$2
TRACT=$3
SEQ=$4
NIGHT=$5
EXPNUM=$6

PATCH=0,0

COADD_RERUN=coadd
PROCESSCCD_RERUN=processCcdOutputs

makeDiscreteSkyMap.py "${REPO}" --rerun "${PROCESSCCD_RERUN}":"${COADD_RERUN}" \
    --id field="${FIELD}" seq=${SEQ} filter=H night=${NIGHT} expnum=${EXPNUM} \
    --config skyMap.projection="TAN" \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --rerun "${COADD_RERUN}" \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

makeCoaddTempExp.py "${REPO}" --rerun "${COADD_RERUN}" \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

assembleCoadd.py "${REPO}" --rerun "${COADD_RERUN}" \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH}

assembleCoadd.py "${REPO}" --rerun "${COADD_RERUN}" \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH}
