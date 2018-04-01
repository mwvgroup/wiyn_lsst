#!/bin/bash

#source /global/homes/k/kap146/.bashrc.wiyn
#export PATH=$PATH:/global/homes/w/wmwv/local/bin

export ASTROMETRY_NET_DATA_DIR="${DR1BASE}/2MASS/2MASS"

#    --id filename='PS1-12bwh_A_J_20121028.lsst.fits' \
#    --id filename='SN2013cb_A_H_20130519.fits'
WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

#    @science_ids_dr2.list \
#    --id field='SN2013cb' seq=A filter=H night=20130519 expnum=210 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131120 expnum=263 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131209 expnum=088 \
#    --id field='iPTF13ebh' seq=A filter=H night=20131213 expnum=137 \
processCcd.py "${REPO}" \
    --id field='LSQ13cwp' seq=A filter=H night=20131111 expnum=521 \
    --id field='LSQ13cwp' seq=A filter=H night=20131120 expnum=335 \
    --id field='LSQ13cwp' seq=A filter=H night=20131209 expnum=312 \
    --id field='LSQ13cwp' seq=A filter=H night=20131213 expnum=274 \
    --id field='LSQ13cwp' seq=A filter=J night=20131111 expnum=562 \
    --id field='LSQ13cwp' seq=A filter=J night=20131120 expnum=425 \
    --id field='LSQ13cwp' seq=A filter=J night=20131209 expnum=335 \
    --id field='LSQ13cwp' seq=A filter=J night=20131213 expnum=299 \
    --configfile config/processCcd.py \
    --output "${REPO}" \
    --clobber-config \
    --clobber-version

#    --loglevel DEBUG \
#    --debug
