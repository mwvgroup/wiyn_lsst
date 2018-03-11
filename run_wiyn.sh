source /global/homes/k/kap146/.bashrc.wiyn
export PATH=$PATH:/global/homes/w/wmwv/local/bin

export ASTROMETRY_NET_DATA_DIR=/project/projectdirs/m1727/cat/2MASS

#    --id filename='PS1-12bwh_A_J_20121028.lsst.fits' \
WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr2

processCcd.py ${REPO} \
    @science_ids_dr2.list \
    --output ${REPO} \
    -C processCcd.config \
    --clobber-config \
    --clobber-version 
