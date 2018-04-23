import os

import matplotlib.pyplot as plt
import numpy as np

from astropy.table import Table

import lsst.afw.display as afwDisplay
import lsst.afw.geom as afwGeom
from lsst.daf.persistence import Butler

from deepcoadd_afw_to_astropy import read_cats

from wiyn_forcedPhotExternalCatalog import assemble_catalogs_into_lightcurve

repo = os.path.join(os.getenv('DR1BASE'), 'repo', 'test_dr1')
rerun = os.path.join(repo, 'rerun', 'forcedPhot')

field, tract = 'PTF11moy', 22

J_cat, H_cat, ref_table = read_cats(field, tract=tract, repo=rerun)

snr_threshold = 5
good_color = (J_cat['J_SNR'] > snr_threshold) & (H_cat['H_SNR'] > snr_threshold)

J_cat = J_cat[good_color]
H_cat = H_cat[good_color]
ref_table = ref_table[good_color]

butler = Butler(rerun)

dId = {'field': field, 'filter': 'H', 'tract': tract, 'patch': '0,0'}
calexp = butler.get('deepCoadd', dataId=dId)


# Find PTF11mty based on RA, Dec: 21:34:05.20, +10:25:24.6 (J2000)

PTF11mty_RA, PTF11mty_Dec = 323.521667, 10.423500

sn_coord = afwGeom.SpherePoint(PTF11mty_RA, PTF11mty_Dec, afwGeom.degrees)

distList = []
for s in ref_table:
    this_coord = afwGeom.SpherePoint(s['coord_ra'], s['coord_dec'], afwGeom.radians)
    angSep = sn_coord.separation(this_coord)
    distList.append(angSep)

distance = np.array(distList)
sn_idx = np.argmin(distance)

print("Found match: Object %d at %f arcsecs" % (sn_idx, afwGeom.radToArcsec(distance[sn_idx])))


# Read in the forced-src photometry files that were built off of this same reference table to extract a lightcurve for PTF11mty

# 2018-04-10:  MWV: This presently doesn't pull the correct expnums for each.
cat_dataRefs = butler.subset(datasetType='forced_src', dataId=dId)

dataIds_by_filter = {}
dataIds_by_filter['H'] = [
    {'field': field, 'seq': 'A', 'filter': 'H', 'night': 20111025, 'expnum': 127},
    ]
dataIds_by_filter['J'] = [
    {'field': field, 'seq': 'A', 'filter': 'J', 'night': 20111025, 'expnum': 109},
    ]

lc = assemble_catalogs_into_lightcurve(dataIds_by_filter, rerun, dataset='forced_src')
lc_file = '{:s}.ecsv'.format(field)
lc.write(lc_file, format='ascii.ecsv', overwrite=True)

lc.pprint(max_width=-1)

filters = ['J', 'H']
colors = {'J': 'blue', 'H': 'green', 'KS': 'red'}
for filt in filters:
    wf, = np.where(lc['filter'] == filt)
    lc_filt = lc[wf]
    plt.errorbar(lc_filt['mjd'], lc_filt['base_PsfFlux_mag'], lc_filt['base_PsfFlux_magSigma'], label=filt,
                marker='o', color=colors[filt], linestyle='none')


ylim = plt.ylim()
plt.ylim(ylim[::-1])

plt.xlabel('MJD')
plt.ylabel('mag')
plt.legend()
plot_file = '{:s}_lc.pdf'.format(field)

plt.savefig(plot_file)
plt.show()

display = afwDisplay.getDisplay(backend='ds9')

display.mtv(calexp)

display.setMaskTransparency(80)
display.scale("asinh", -2, 25)

X = 'slot_Centroid_x'
Y = 'slot_Centroid_y'

display.erase()


with display.Buffering():
    for s in ref_table:
        display.dot("o", s[X], s[Y], size=10, ctype='orange')

sn_ref = ref_table[sn_idx]
display.dot("o", sn_ref[X], sn_ref[Y], size=20, ctype='green')

