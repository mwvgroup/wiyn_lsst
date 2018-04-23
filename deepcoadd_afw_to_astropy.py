import os

import lsst.daf.persistence as dafPersist

# See https://pipelines.lsst.io/getting-started/multiband-analysis.html

DR1BASE = os.getenv("DR1BASE")
REPO = os.path.join(DR1BASE, 'repo', 'test_dr1')

def read_cats(field, tract, repo=REPO, datasetType='deepCoadd_forced_src'):
    butler = dafPersist.Butler(repo)

    dId_H = {'field': field, 'tract': tract, 'patch': '0,0', 'filter': 'H'}
    H_cat = butler.get(datasetType, dId_H)
    dId_J = {'field': field, 'tract': tract, 'patch': '0,0', 'filter': 'J'}
    J_cat = butler.get(datasetType, dId_J)

    HCoaddCalib = butler.get('deepCoadd_calexp_calib', dId_H)
    JCoaddCalib = butler.get('deepCoadd_calexp_calib', dId_J)

    HCoaddCalib.setThrowOnNegativeFlux(False)
    JCoaddCalib.setThrowOnNegativeFlux(False)

    H_mag, H_mag_err = HCoaddCalib.getMagnitude(H_cat['base_PsfFlux_flux'], H_cat['base_PsfFlux_fluxSigma'])
    J_mag, J_mag_err = JCoaddCalib.getMagnitude(J_cat['base_PsfFlux_flux'], J_cat['base_PsfFlux_fluxSigma'])

    ref_table = butler.get('deepCoadd_ref', {'filter': 'H^J', 'tract': tract, 'patch': '0,0'})
    isPrimary = ref_table['detect_isPrimary']

    H_table = H_cat.asAstropy(copy=True)
    J_table = J_cat.asAstropy(copy=True)
    ref_table = ref_table.asAstropy(copy=True)

    H_table['H_mag'] = H_mag
    J_table['J_mag'] = J_mag
    H_table['H_mag_err'] = H_mag_err
    J_table['J_mag_err'] = J_mag_err
    H_table['H_SNR'] = H_cat['base_PsfFlux_flux']/H_cat['base_PsfFlux_fluxSigma']
    J_table['J_SNR'] = J_cat['base_PsfFlux_flux']/J_cat['base_PsfFlux_fluxSigma']

    H_table = H_table[isPrimary]
    J_table = J_table[isPrimary]
    ref_table = ref_table[isPrimary]

    return J_table, H_table, ref_table


def run(field, tract):
    J_cat, H_cat, ref_cat = read_cats(field=field, tract=tract)

    H_cat.write('%s_H_cat.fits' % field, overwrite=True)
    J_cat.write('%s_J_cat.fits' % field, overwrite=True)
    ref_cat.write('%s_ref_cat.fits' % field, overwrite=True)


if __name__ == "__main__":
    run(field='LSQ13cwp', tract=0)
    run(field='PTF11mty', tract=1)
