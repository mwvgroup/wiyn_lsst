#!/bin/bash

#source /global/homes/k/kap146/.bashrc.wiyn
#export PATH=$PATH:/global/homes/w/wmwv/local/bin

export ASTROMETRY_NET_DATA_DIR="${DR1BASE}/2MASS/2MASS"

#    --id filename='PS1-12bwh_A_J_20121028.lsst.fits' \
#    --id filename='SN2013cb_A_H_20130519.fits'
WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

#    @science_ids_dr2.list \
processCcd.py "${REPO}" \
    --id field='SN2013cb' seq=A filter=H night=20130519 expnum=210 \
    --output "${REPO}"
