import os

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

base_dir = os.path.join(os.getenv('HOME'), "local/lsst/wiyn_lsst")
dataset_name = "2MASS"

config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.astromRefObjLoader.ref_dataset_name = dataset_name
config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.photoRefObjLoader.ref_dataset_name = dataset_name
config.calibrate.photoCal.photoCatName = dataset_name

# The edges are low S/N regimes and are likely to have plenty of single-pixel excursions
# One way to deal with this is to set the number of allowed CRs really high
config.charImage.repair.cosmicray.nCrPixelMax = 1000000

# Skip Astrometry for right now
config.calibrate.doAstrometry=False

# Astrometry settings
config.charImage.ref_match.matcher.maxOffsetPix=800
config.charImage.ref_match.matcher.maxRotationDeg=0
config.charImage.ref_match.matcher.allowedNonperpDeg=0

# Astrometry and Photometry Catalog
filternames = ('J', 'H', 'Ks', 'KS', 'WHIRCJ', 'WHIRCH', 'WHIRCK', 'WHIRCKS')
filters = ('J', 'H', 'K', 'K', 'J', 'H', 'K', 'K')

for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader,
                     ):
    for fn, f in zip(filternames, filters):
        refObjLoader.filterMap[fn] = f

# filterMapFile = os.path.join(base_dir, "ref_cats", "2MASS", "filterMap.py")
# for refObjLoader in (config.calibrate.astromRefObjLoader,
#                      config.calibrate.photoRefObjLoader,
#                      config.charImage.refObjLoader,
#                      ):
#     refObjLoader.load(filterMapFile)
# 
