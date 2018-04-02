#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

detectCoaddSources.py "${REPO}" --output "${REPO}" \
    --id field=PTF11mty filter=H \
    --id field=PTF11mty filter=J \
    --clobber-versions

mergeCoaddDetections.py "${REPO}" --output "${REPO}" \
    --id field=PTF11mty filter=H^J \
    --configfile config/mergeCoaddDetections.py \
    --clobber-versions

measureCoaddSources.py "${REPO}" --output "${REPO}" \
    --id field=PTF11mty filter=H^J \
    --clobber-versions 
