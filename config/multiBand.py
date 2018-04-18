import os

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

base_dir = os.path.join(os.getenv('HOME'), "local/lsst/wiyn_lsst")
dataset_name = "2MASS"

config.measureCoaddSources.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.measureCoaddSources.match.refObjLoader.ref_dataset_name = dataset_name

# Astrometry and Photometry Catalog
filternames = ('J', 'H', 'Ks', 'KS', 'WHIRCJ', 'WHIRCH', 'WHIRCK', 'WHIRCKS')
filters = ('J', 'H', 'K', 'K', 'J', 'H', 'K', 'K')

for refObjLoader in (config.measureCoaddSources.match.refObjLoader,):
    for fn, f in zip(filternames, filters):
        refObjLoader.filterMap[fn] = f

config.measureCoaddSources.doPropagateFlags = False

config.mergeCoaddDetections.priorityList = ['H', 'J']
config.mergeCoaddMeasurements.priorityList = ['H', 'J']
