source ~/.bashrc.lsst

setup lsst_apps
setup -k -r ~wmwv/lsst/obs_file

TMP=${HOME}/tmp
REPO=${TMP}/test_dr1
mkdir -p ${REPO}
echo "lsst.obs.file.FileMapper" > ${REPO}/_mapper

# python wiynAssembleExp.py ${DR1BASE}/stacks/*[0-9].fits
# python wiynAssembleExp.py ${DR1BASE}/stacks/PS1-12bwh_A_*[0-9].fits

# ingestFiles.py ${REPO} ${DR1BASE}/stacks/PS1-12bwh_A_*.lsst.fits
#ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits
ingestFiles.py ${REPO} ${DR1BASE}/*.lsst.fits
