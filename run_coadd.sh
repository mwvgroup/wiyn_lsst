#!/bin/bash

REPO=$1
FIELD=$2
TRACT=$3
SEQ=$4
NIGHT=$5

PATCH=0,0

COADD_RERUN=coadd
PROCESSCCD_RERUN=processCcd

# We make coadds in both J, H by default.
# We define the DiscreteSkyMap in terms of the H filter.
# That means that what we pass in should be in terms of the H filter.
makeDiscreteSkyMap.py "${REPO}" --rerun "${PROCESSCCD_RERUN}":"${COADD_RERUN}" \
    --id field="${FIELD}" seq=${SEQ} filter=H night=${NIGHT} \
    --config skyMap.projection="TAN" \
    --clobber-versions

# The following explicitly iterate between H, J
# for the given FIELD+TRACT.
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
