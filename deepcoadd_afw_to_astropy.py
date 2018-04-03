import os

import lsst.daf.persistence as dafPersist

# See https://pipelines.lsst.io/getting-started/multiband-analysis.html

dr1base = os.getenv("DR1BASE")
repo = os.path.join(dr1base, "tmp", "test_dr1")

butler = dafPersist.Butler(repo)

dId_H = {'field': 'PTF11mty', 'tract': 1, 'patch': '0,0', 'filter': 'H'}
H_cat = butler.get('deepCoadd_forced_src', dId_H)
dId_J = {'field': 'PTF11mty', 'tract': 1, 'patch': '0,0', 'filter': 'J'}
J_cat = butler.get('deepCoadd_forced_src', dId_J)

HCoaddCalib = butler.get('deepCoadd_calexp_calib', dId_H)
JCoaddCalib = butler.get('deepCoadd_calexp_calib', dId_J)

HCoaddCalib.setThrowOnNegativeFlux(False)
JCoaddCalib.setThrowOnNegativeFlux(False)

H_mag, H_mag_err = HCoaddCalib.getMagnitude(H_cat['base_PsfFlux_flux'], H_cat['base_PsfFlux_fluxSigma'])
J_mag, J_mag_err = JCoaddCalib.getMagnitude(J_cat['base_PsfFlux_flux'], J_cat['base_PsfFlux_fluxSigma'])

refTable = butler.get('deepCoadd_ref', {'filter': 'H^J', 'tract': 1, 'patch': '0,0'})
isPrimary = refTable['detect_isPrimary']

H_table = H_cat.asAstropy(copy=True)
J_table = J_cat.asAstropy(copy=True)

H_table['H_mag'] = H_mag
J_table['J_mag'] = J_mag
H_table['H_mag_err'] = H_mag_err
J_table['J_mag_err'] = J_mag_err
H_table['H_SNR'] = H_cat['base_PsfFlux_flux']/H_cat['base_PsfFlux_fluxSigma']
J_table['J_SNR'] = J_cat['base_PsfFlux_flux']/J_cat['base_PsfFlux_fluxSigma']

H_table = H_table[isPrimary]
J_table = J_table[isPrimary]

H_table.write('PTF11mty_H_cat.fits', overwrite=True)
J_table.write('PTF11mty_J_cat.fits', overwrite=True)
