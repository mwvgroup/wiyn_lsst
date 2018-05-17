import os

import numpy as np

import lsst.daf.persistence as dafPersist
from lsst.daf.persistence import butlerExceptions

# See https://pipelines.lsst.io/getting-started/multiband-analysis.html

DR1BASE = os.getenv("DR1BASE")
REPO = os.path.join(DR1BASE, 'repo', 'test_dr1')
RERUN = os.path.join(REPO, 'rerun', 'forcedPhot')

def read_cats(field, tract, filters = ('J', 'H', 'KS'),
              repo=RERUN, datasetType='deepCoadd_forced_src'):
    """Return the coadd reference catalog and a list of the individual per-filter coadd catalogs."""
    butler = dafPersist.Butler(repo)

    ref_table = butler.get('deepCoadd_ref', {'filter': 'H^J', 'tract': tract, 'patch': '0,0'})
    ref_table = ref_table.asAstropy(copy=True)

    isPrimary = ref_table['detect_isPrimary']

    tables = []
    for f in filters:
        dId = {'field': field, 'tract': tract, 'patch': '0,0', 'filter': f}
        try:
            cat = butler.get(datasetType, dId)
        except butlerExceptions.NoResults:
            continue

        CoaddCalib = butler.get('deepCoadd_calexp_calib', dId)
        CoaddCalib.setThrowOnNegativeFlux(False)

        mag, mag_err = CoaddCalib.getMagnitude(cat['base_PsfFlux_flux'], cat['base_PsfFlux_fluxSigma'])

        tab = cat.asAstropy(copy=True)
        tab.meta['filter'] = f

        tab['%s_mag' % f] = mag
        tab['%s_mag_err' % f] = mag_err
        tab['%s_SNR' % f] = np.abs(cat['base_PsfFlux_flux'])/cat['base_PsfFlux_fluxSigma']

        tab = tab[isPrimary]
        tables.append(tab)

    ref_table = ref_table[isPrimary]

    return ref_table, tables


def run(field, tract):
    ref_cat, cats = read_cats(field=field, tract=tract)

    ref_cat.write('%s_ref_cat.fits' % field, overwrite=True)
    for cat in cats:
        filt = cat.meta['filter']
        cat.write('%s_%s_cat.fits' % (field, filt), overwrite=True)


if __name__ == "__main__":
    run(field='LSQ13cwp', tract=14)
    run(field='PTF11mty', tract=23)
