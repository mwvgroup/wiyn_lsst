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

# We make coadds in both J, H by default.
# We define the DiscreteSkyMap in terms of the H filter.
# That means that what we pass in should be in terms of the H filter.
makeDiscreteSkyMap.py "${REPO}" --rerun "${PROCESSCCD_RERUN}":"${COADD_RERUN}" \
    --id field="${FIELD}" seq=${SEQ} filter=${FILTER} night=${NIGHT} \
    --config skyMap.projection="TAN" \
    --clobber-versions
