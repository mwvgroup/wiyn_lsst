source ~/.bashrc.lsst

setup lsst_apps
setup -k -r ~/local/lsst/obs_file

ingestFiles.py ${REPO} ${DR1BASE}/stacks/*.lsst.fits
