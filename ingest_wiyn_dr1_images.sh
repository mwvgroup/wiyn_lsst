source ~/.bashrc.wiyn

setup lsst_apps
setup -k -r /global/homes/w/wmwv/local/lsst/obs_file

TMP=${DR1BASE}/tmp
REPO=${TMP}/test_dr1
mkdir -p ${REPO}
echo "lsst.obs.file.FileMapper" > ${REPO}/_mapper

ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits

sqlite3 ${REPO}/registry.sqlite3 "UPDATE raw SET filter = substr(fileroot, -10, 1) ;"
