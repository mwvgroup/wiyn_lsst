#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

cut -f 1 -d ' ' dr1_coadd.list > dr1_field.list

while read field; do
    echo bash run_photometry.sh "${REPO}" "${field}"
done < dr1_field.list
