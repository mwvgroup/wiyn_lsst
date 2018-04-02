import os

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

base_dir = os.path.join(os.getenv('HOME'), "local/lsst/wiyn_lsst")
dataset_name = "2MASS"

config.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.match.refObjLoader.ref_dataset_name = dataset_name

# Astrometry and Photometry Catalog
filternames = ('J', 'H', 'Ks', 'KS', 'WHIRCJ', 'WHIRCH', 'WHIRCK', 'WHIRCKS')
filters = ('J', 'H', 'K', 'K', 'J', 'H', 'K', 'K')

for refObjLoader in (config.match.refObjLoader,):
    for fn, f in zip(filternames, filters):
        refObjLoader.filterMap[fn] = f

# filterMapFile = os.path.join(base_dir, "ref_cats", "2MASS", "filterMap.py")
# for refObjLoader in (config.calibrate.astromRefObjLoader,
#                      config.calibrate.photoRefObjLoader,
#                      config.charImage.refObjLoader,
#                      ):
#     refObjLoader.load(filterMapFile)
# 
