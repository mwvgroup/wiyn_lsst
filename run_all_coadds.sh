#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

while read -r line; do
    bash run_coadd.sh "${REPO}" ${line}
done < dr1_coadd.list
