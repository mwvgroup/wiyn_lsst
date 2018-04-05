#!/bin/bash

REPO=$1
FIELD=$2

# Should be able to replace all of this with multiBandDriver.py
# But it was useful to go through step by step to get it all working.
detectCoaddSources.py "${REPO}" --rerun coadd:coaddPhot \
    --id field="${FIELD}" filter=H \
    --id field="${FIELD}" filter=J \
    --clobber-versions

mergeCoaddDetections.py "${REPO}" --rerun coaddPhot \
    --id field="${FIELD}" filter=H^J \
    --configfile config/mergeCoaddDetections.py \
    --clobber-versions

measureCoaddSources.py "${REPO}" --rerun coaddPhot \
    --id field="${FIELD}" filter=H^J \
    --configfile config/measureCoaddSources.py \
    --clobber-versions 

mergeCoaddMeasurements.py "${REPO}" --rerun coaddPhot \
    --id field="${FIELD}" filter=H^J \
    --configfile config/mergeCoaddDetections.py \
    --clobber-versions

forcedPhotCoadd.py "${REPO}" --rerun coaddPhot \
    --id field="${FIELD}" filter=H^J \
    --clobber-versions
