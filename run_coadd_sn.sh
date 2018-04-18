#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

sn=$1

grep ${sn} dr1_coadd_actual.list > dr1_coadd_${sn}.list

while read -r line; do
    . run_coadd.sh "${REPO}" ${line}
done < dr1_coadd_${sn}.list
