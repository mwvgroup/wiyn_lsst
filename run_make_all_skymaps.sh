#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

# We make coadds in both J, H by default.
# We define the DiscreteSkyMap in terms of the H filter.
# That means that what we pass in should be in terms of the H filter.
while read -r line; do
    . make_skymap.sh "${REPO}" ${line}
done < dr1_coadd_actual.list
