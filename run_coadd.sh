#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

makeDiscreteSkyMap.py "${REPO}" --output "${REPO}" \
    --id field='LSQ13cwp' seq=A filter=H night=20131111 expnum=521 \
    --config skyMap.projection="TAN" \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --output "${REPO}" \
    --selectId filter=H --id field='LSQ13cwp' filter=H tract=0 patch=0,0 \
    --config doApplyUberCal=False \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --output "${REPO}" \
    --selectId filter=J --id field='LSQ13cwp' filter=J tract=0 patch=0,0 \
    --config doApplyUberCal=False \
    --clobber-versions

assembleCoadd.py "${REPO}" --output "${REPO}" \
    --selectId filter=H --id field='LSQ13cwp' filter=H tract=0 patch=0,0 \
    --clobber-versions

assembleCoadd.py "${REPO}" --output "${REPO}" \
    --selectId filter=J --id field='LSQ13cwp' filter=J tract=0 patch=0,0 \
    --clobber-versions

###
makeDiscreteSkyMap.py "${REPO}" --output "${REPO}" \
    --id field='PTF11mty' seq=A filter=H night=20111025 expnum=218 \
    --config skyMap.projection="TAN" \
    --config doAppend="True" \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --output "${REPO}" \
    --selectId filter=H --id field='PTF11mty' filter=H tract=1 patch=0,0 \
    --config doApplyUberCal=False \
    --clobber-versions

makeCoaddTempExp.py "${REPO}" --output "${REPO}" \
    --selectId filter=J --id field='PTF11mty' filter=J tract=1 patch=0,0 \
    --config doApplyUberCal=False \
    --clobber-versions

assembleCoadd.py "${REPO}" --output "${REPO}" \
    --selectId filter=H --id field='PTF11mty' filter=H tract=1 patch=0,0 \
    --clobber-versions

assembleCoadd.py "${REPO}" --output "${REPO}" \
    --selectId filter=J --id field='PTF11mty' filter=J tract=1 patch=0,0 \
    --clobber-versions
