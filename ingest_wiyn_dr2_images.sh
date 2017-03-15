#source /global/homes/k/kap146/.bashrc.lsst
source /global/homes/w/wmwv/.bashrc.wiyn
DR2BASE=/global/project/projectdirs/lsst/wmwv/test/DR2_images_rc1
export PATH=$PATH:/global/homes/w/wmwv/local/bin
export PATH=$PATH:/global/homes/w/wmwv/local/lsst/obs_file

setup lsst_apps
setup -k -r /global/homes/w/wmwv/local/lsst/obs_file

#SCRATCH=/global/cscratch1/sd/kap146
TMP=${SCRATCH}/tmp
REPO=${TMP}/test_dr2
mkdir -p ${REPO}
echo "lsst.obs.file.FileMapper" > ${REPO}/_mapper

ingestFiles.py ${REPO} ${DR2BASE}/stacks/*.lsst.fits

sqlite3 ${REPO}/registry.sqlite3 "UPDATE raw SET filter = substr(fileroot, -10, 1) ;"
