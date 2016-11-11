#!/usr/bin/env python
import os

from astropy.table import Table

import lsst.daf.persistence as dafPersist

from forcedPhotExternalCatalog import ForcedPhotExternalCatalogTask
from sub_wiyn_dr1 import sn_with_dr1_templates, repo_dir, find_science_images, filename_to_fileroot


def run_forced_photometry(science_fileroot, coord_file, repo_dir, dataset='calexp', verbose=True):
    science_fileroot = filename_to_fileroot(science_file)
    args = [repo_dir,
            '--id', 'fileroot={}'.format(science_fileroot),
            '--dataset', '{}'.format(dataset),
            '--coord_file', '{}'.format(coord_file),
            '--output', '{}'.format(repo_dir),
            '--clobber-config', '--clobber-versions',
           ]
    if verbose:
        print(args)
    ForcedPhotExternalCatalogTask.parseAndRun(args=args)


def extract_forced_photometry(butler, fileroot):
    """Return the data from the forced photometry."""
    dataset = 'forced_src'
    catalog = butler.get(dataset, dataId={'fileroot': fileroot})
    return catalog


def assemble_catalogs_into_lightcurve(science_fileroots, repo_dir):
    """Return Table with measurements."""
    butler = dafPersist.Butler(repo_dir)

    names_to_copy = ['objectId', 'coord_ra', 'coord_dec', 'parentObjectId',
                     'base_RaDecCentroid_x', 'base_RaDecCentroid_y',
                     'base_PsfFlux_flux', 'base_PsfFlux_fluxSigma']
    names_to_generate = ['filter', 'mjd']

    names = names_to_generate + names_to_copy
    dtype = (str, float, long, float, float, long, float, float, float, float)
    table = Table(names=names, dtype=dtype)

    for f, fileroots in science_fileroots.items():
        for fileroot in fileroots:
            dataId = {'fileroot': fileroot}
            # Can grab filter, mjd from 'calexp_mc' call on fileroot
            md = butler.get('calexp_md', dataId=dataId, immediate=True)
            mjd = md.get('MJD-OBS')
            # md.get('FILTER')  # But that's not being set right now so we'll keep using f

            this_measurement = extract_forced_photometry(butler, fileroot)
            # 'this_measurement' is a table, but we're only extracting the first entry from each column
            cols_for_new_row = {n: this_measurement[n][0] for n in names_to_copy}
            cols_for_new_row['filter'] = f
            cols_for_new_row['mjd'] = mjd
            table.add_row(cols_for_new_row)

    return table


def test_assemble_catalogs_into_lightcurves():
    """Needs to have a run already existing to work."""
    # repo_dir  # From Global import above
    science_fileroots = {'H': [
        'SN2011gy_A_H_20111115',
        'SN2011gy_A_H_20111121',
        'SN2011gy_A_H_20111208',
        'SN2011gy_A_H_20120108',
        'SN2011gy_A_H_20120402'
        ]}
    obs = assemble_catalogs_into_lightcurve(science_fileroots, repo_dir)
    print(obs)


def test_find_science_images(name='SN2011gy', verbose=True):
    """Did our search find any image."""
    for f in ('H'):
        obs = find_science_images(name, f, repo_dir)

    if verbose:
        print(obs)

    assert len(obs) >= 1


if __name__ == "__main__":
    for name, sn in sn_with_dr1_templates.items():
        coord_file = '{}_ra_dec.txt'.format(name)
        out_file = '{}_lc.fits'.format(name)

        print("Processing photometry for {}".format(name))
        lightcurve_fileroots_for_sn = {}
        for f in sn.keys():
#        for f in 'H':
            lightcurve_fileroots_for_sn[f] = []
            template_file = os.path.join(repo_dir, 'calexp', sn[f])
            for science_file in find_science_images(name, f, repo_dir):
                if science_file == template_file:
                    continue
                science_fileroot = filename_to_fileroot(science_file)
                lightcurve_fileroots_for_sn[f].append(science_fileroot)
                run_forced_photometry(science_file, coord_file, repo_dir)

        sn_lc = assemble_catalogs_into_lightcurve(lightcurve_fileroots_for_sn, repo_dir)
        sn_lc.write(out_file, overwrite=True)
