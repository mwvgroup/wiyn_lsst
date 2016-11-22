source ~/.bashrc.wiyn

export ASTROMETRY_NET_DATA_DIR=/project/projectdirs/m1727/cat/2MASS

#    --id filename='PS1-12bwh_A_J_20121028.lsst.fits' \
WIYN=${HOME}/tmp
REPO=${WIYN}/test_dr1

processCcd.py ${REPO} \
    @science_ids.list \
    --output ${REPO} \
    -C processCcd.config \
    --clobber-config \
    --clobber-version 
