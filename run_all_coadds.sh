#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

while read -r line; do
    . run_coadd.sh "${REPO}" ${line}
done < dr1_coadd_actual.list
