#!/bin/bash

WIYN=${DR1BASE}/repo
REPO=${WIYN}/test_dr1

join dr1_sn_lc.txt dr1_coadd_actual.list > dr1_sn_lc_actual.txt

fields=`cat dr1_sn_lc_actual.txt | cut -f 1 -d ' '`

python sn_lightcurve.py $fields
