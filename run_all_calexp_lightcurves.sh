#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

join dr1_sn_lc.txt dr1_coadd_actual.list > dr1_sn_lc_actual.txt

while read field tract seq filter night; do
    python sn_lightcurve.py ${field}
done < dr1_sn_lc_actual.txt
