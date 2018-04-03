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

config.doPropagateFlags = False
