#!/bin/bash

# Performanced forced-position photometry on all stacks covered by
# the tract of a given coadd

REPO=$1
FIELD=$2
TRACT=$3

# Need the individual stack dataIds.

forcedPhotCcd.py "${REPO}" --rerun forcedPhot \
    --id field="${FIELD}" tract=${TRACT} filter=H^J \
    --clobber-versions
