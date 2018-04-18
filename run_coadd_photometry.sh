#!/bin/bash

REPO=$1
FIELD=$2
TRACT=`grep ${FIELD} dr1_field_tract.list | cut -f 2 -d ' '`

COADD_RERUN=coadd
COADDPHOT_RERUN=coaddPhot

multiBandDriver.py \
  "${REPO}" --rerun "${COADD_RERUN}":"${COADDPHOT_RERUN}" \
  --id field=${FIELD} tract=${TRACT} patch=0,0 filter=H^J \
  --configfile config/multiBand.py \
  --cores 4 \
  --clobber-versions

# Should be able to replace all of this with multiBandDriver.py
# But it was useful to go through step by step to get it all working.
#
# detectCoaddSources.py "${REPO}" --rerun "${COADD_RERUN}":"${COADDPHOT_RERUN}" \
#     --id field="${FIELD}" tract=${TRACT} filter=H \
#     --id field="${FIELD}" tract=${TRACT} filter=J \
#     --clobber-versions
# 
# mergeCoaddDetections.py "${REPO}" --rerun "${COADDPHOT_RERUN}" \
#     --id field="${FIELD}" tract=${TRACT} filter=H^J \
#     --configfile config/mergeCoaddDetections.py \
#     --clobber-versions
# 
# measureCoaddSources.py "${REPO}" --rerun "${COADDPHOT_RERUN}" \
#     --id field="${FIELD}" tract=${TRACT} filter=H^J \
#     --configfile config/measureCoaddSources.py \
#     --clobber-versions 
# 
# mergeCoaddMeasurements.py "${REPO}" --rerun "${COADDPHOT_RERUN}" \
#     --id field="${FIELD}" tract=${TRACT} filter=H^J \
#     --configfile config/mergeCoaddDetections.py \
#     --clobber-versions
# 
# forcedPhotCoadd.py "${REPO}" --rerun "${COADDPHOT_RERUN}" \
#     --id field="${FIELD}" tract=${TRACT} filter=H^J \
#     --clobber-versions
