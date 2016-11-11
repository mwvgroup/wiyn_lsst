source ~/.bashrc.lsst

setup lsst_apps
setup -k -r ~/local/lsst/obs_file

TMP=${HOME}/tmp
REPO=${TMP}/test_dr1
mkdir -p ${REPO}

ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits
