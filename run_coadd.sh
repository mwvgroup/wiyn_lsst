#!/bin/bash

REPO=$1
FIELD=$2
TRACT=$3
NIGHT=$4
EXPNUM=$5

SEQ=A
PATCH=0,0

makeDiscreteSkyMap.py "${REPO}" --rerun processCcdOutputs:coadd \
    --id field="${FIELD}" seq=${SEQ} filter=H night=${NIGHT} expnum=${EXPNUM} \
    --config skyMap.projection="TAN" \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --rerun coadd \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

makeCoaddTempExp.py "${REPO}" --rerun coadd \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH} \
    --config doApplyUberCal=False

assembleCoadd.py "${REPO}" --rerun coadd \
    --selectId filter=H --id field="${FIELD}" filter=H tract=${TRACT} patch=${PATCH}

assembleCoadd.py "${REPO}" --rerun coadd \
    --selectId filter=J --id field="${FIELD}" filter=J tract=${TRACT} patch=${PATCH}
