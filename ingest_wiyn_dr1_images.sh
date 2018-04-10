# source ~/.bashrc.wiyn
#
# setup lsst_apps
# setup -k -r ~wmwv/local/lsst/obs_wiyn

REPO="${DR1BASE}"/repo/test_dr1
mkdir -p "${REPO}"
echo "lsst.obs.wiyn.WhircMapper" > "${REPO}"/_mapper

ln -s "${DR1BASE}"/ref_cats "${REPO}"/ref_cats

ingestImages.py "${REPO}" "${DR1BASE}"/stacks/*.lsst.fits --mode link \
    --configfile "${OBS_WIYN_DIR}"/config/ingestStack.py

## I think we get the filters right now.
# sqlite3 ${REPO}/registry.sqlite3 "UPDATE raw SET filter = substr(fileroot, -10, 1) ;"
