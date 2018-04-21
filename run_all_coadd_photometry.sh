#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

cut -f 1,2 -d ' ' dr1_coadd_actual.list > dr1_field_tract.list

while read line; do
    . run_coadd_photometry.sh "${REPO}" ${line}
done < dr1_field_tract.list
