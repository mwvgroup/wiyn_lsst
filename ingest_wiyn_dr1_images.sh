source /global/homes/k/kap146/.bashrc.wiyn
DR1BASE=/global/project/projectdirs/lsst/wmwv/test/DR1_images_rc3
export PATH=$PATH:/global/homes/w/wmwv/local/bin

setup lsst_apps
setup -k -r /global/homes/w/wmwv/local/lsst/obs_file

#SCRATCH=/global/cscratch1/sd/kap146
TMP=${SCRATCH}/tmp
REPO=${TMP}/test_dr1
mkdir -p ${REPO}
echo "lsst.obs.file.FileMapper" > ${REPO}/_mapper

ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits

sqlite3 ${REPO}/registry.sqlite3 "UPDATE raw SET filter = substr(fileroot, -10, 1) ;"
