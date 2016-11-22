source ~/.bashrc.lsst

setup lsst_apps
setup -k -r ~wmwv/local/lsst/obs_file

TMP=${HOME}/tmp
REPO=${TMP}/test_dr1
mkdir -p ${REPO}
echo "lsst.obs.file.FileMapper" > ${REPO}/_mapper

ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits
