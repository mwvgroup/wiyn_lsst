#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

# Should be able to replace all of this with multiBandDriver.py
# But it was useful to go through step by step to get it all working.
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
    --configfile config/measureCoaddSources.py \
    --clobber-versions 

mergeCoaddMeasurements.py "${REPO}" --output "${REPO}" \
    --id field=PTF11mty filter=H^J \
    --configfile config/mergeCoaddDetections.py \
    --clobber-versions

forcedPhotCoadd.py "${REPO}" --output "${REPO}" \
    --id field=PTF11mty filter=H^J \
    --clobber-versions
