#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

makeDiscreteSkyMap.py "${REPO}" --output "${REPO}" \
    --id field='LSQ13cwp' seq=A filter=H night=20131111 expnum=521 \
    --config skyMap.projection="TAN" \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --output "${REPO}" \
    --selectId filter=H --id filter=H tract=0 patch=0,0^0,1^0,0^1,1 \
    --config doApplyUberCal=False \
    --clobber-versions

assembleCoadd.py "${REPO}" --output "${REPO}" \
    --select ID filter=H \
    --selectId filter=H --id filter=H tract=0 patch=0,0^0,1^0,0^1,1 \
    --clobber-versions
