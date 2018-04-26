#!/usr/bin/env python

from __future__ import print_function, division

from collections import OrderedDict

import numpy as np

from astropy.table import Table
import astropy.units as u

import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils
import lsst.daf.persistence as dafPersist

from forcedPhotExternalCatalog import ForcedPhotExternalCatalogTask
from sub_wiyn_dr1 import sn_with_dr1_templates, repo_dir, find_science_images, filename_to_fileroot


def run_forced_photometry(dataId, coord_file, repo_dir, dataset='calexp',
                          verbose=True):
    print(dataId)
    # Should expand out dataId to be more detailed than just visit.
    args = [repo_dir,
            '--id', 'fileroot={:s}'.format(dataId['fileroot']),
            '--dataset', '{}'.format(dataset),
            '--coord_file', '{}'.format(coord_file),
            '--output', '{}'.format(repo_dir),
            '--clobber-config', '--clobber-versions',
           ]
    if verbose:
        print(args)
    ForcedPhotExternalCatalogTask.parseAndRun(args=args)


def extract_photometry(butler, dataId, forced_dataset, filt, source_row, names_to_copy,
                       phot_type='base_PsfFlux'):
    # Can grab filter, mjd from 'calexp_md' call on visit
    md = butler.get('calexp_md', dataId=dataId, immediate=True)
    mjd = md.get('MJD-OBS')
#        filt = md.get('FILTER')  # But that's not being set right now so we'll keep using f

    this_measurement = butler.get(forced_dataset, dataId)
    # 'this_measurement' is a table, but we're only extracting the first entry from each column
    new_row = {n: this_measurement[n][source_row] for n in names_to_copy}
#        new_row['filter'] = dataId['filter']
    new_row['filter'] = filt
    new_row['mjd'] = mjd

    # Calibrate to magnitudes
    # The calibration information for the calexp
    # should still apply to the difference image
    calib = afwImage.Calib(md)
    with afwImageUtils.CalibNoThrow():
        new_row['%s_mag' % phot_type], new_row['%s_magSigma' % phot_type] = \
            calib.getMagnitude(new_row['%s_flux' % phot_type],
                               new_row['%s_fluxSigma' % phot_type])
    flux_mag_0, flux_magSigma_0 = calib.getFluxMag0()
    flux_mag_25 = 10**(-0.4*25) * flux_mag_0
    flux_norm = 1/flux_mag_25
    new_row['%s_flux_zp25' % phot_type] = \
        flux_norm * new_row['%s_flux' % phot_type]
    new_row['%s_fluxSigma_zp25' % phot_type] = \
        flux_norm * new_row['%s_fluxSigma' % phot_type]
    return new_row


def assemble_catalogs_into_lightcurve(dataIds_by_filter, repo_dir, source_row=0,
                                      phot_type='base_PsfFlux', dataset='calexp',
                                      debug=False):
    """Return Table with measurements."""
    butler = dafPersist.Butler(repo_dir)

    names_to_copy = ['objectId', 'coord_ra', 'coord_dec', 'parentObjectId',
                     '%s_flux' % phot_type, '%s_fluxSigma' % phot_type]
    # flux_zp25 is flux normalized to a zeropoint of 25.
    # This convention is useful and appropriate for transient sources
    # that are expected to be negative as well as positive
    # for a given lightcurve.
    names_to_generate = ['filter', 'mjd',
                         '%s_mag' % phot_type, '%s_magSigma' % phot_type,
                         '%s_flux_zp25' % phot_type, '%s_fluxSigma_zp25' % phot_type]
    names = names_to_generate + names_to_copy
    dtype = (str, float,
             float, float,
             float, float, int,
             float, float,
             int,
             float, float)

    units = (None, u.d,
             u.mag, u.mag,
             None, None,
             None, u.rad, u.rad, None,
             None, None)

    table = Table(names=names, dtype=dtype)

    if dataset == 'deepDiff_differenceExp':
        prefix = 'deepDiff_'
    else:
        prefix = ''
    forced_dataset = prefix+'forced_src'
    if debug:
        print("FORCED_DATASET: ", forced_dataset)

    for f, dataIds in dataIds_by_filter.items():
        for dataId in dataIds:
            try:
                new_row = extract_photometry(butler, dataId, forced_dataset, f, source_row,
                                             names_to_copy, phot_type=phot_type )
            except Exception as e:
                print(e)
                print("Unable to extract forced photometry from {}".format(dataId))
                continue
            table.add_row(new_row)

    for n, unit in zip(names, units):
        if unit is not None:
            table[n].unit = unit

    return table


def test_assemble_catalogs_into_lightcurves():
    """Needs to have a run already existing to work."""
    # repo_dir  # From Global import above
    science_visits = {'r': ['255276', '2221459']}
    obs = assemble_catalogs_into_lightcurve(science_visits, repo_dir)
    print(obs)


def test_find_science_images(name='Test1', verbose=True):
    """Did our search find any image."""
    for f in ('r'):
        obs = find_science_images(name, f, repo_dir)

    if verbose:
        print(obs)

    assert len(obs) >= 1


def make_catalogs(lightcurve_visits_for_sn, repo_dir, dataset='calexp'):
    this_row = 0
    for name, info in lightcurve_visits_for_sn.items():
        try:
            out_file = '{}_{}_lc.fits'.format(name, dataset)
            sn_lc = assemble_catalogs_into_lightcurve(info, repo_dir, this_row, dataset=dataset)
            sn_lc.write(out_file, overwrite=True)
        except Exception as e:
            print(e)
            print("Failed to generate lightcurve for {}".format(name))


def run_photometry_for_coord_file(coord_file, repo_dir, dataset='calexp',
                                  filters=None, run_phot=True, limit_n=None, debug=False):
    """Run photometry for all objects in a coordinate file on all available images.

    run_phot : Run photometry.  If False then photometry is not run, but visits are gathered
    """
    # Can't put mutable as default argument above without much sadness.
    if filters is None:
        filters = ['u', 'g', 'r', 'i', 'z', 'y']

    objects = Table.read(coord_file, format='ascii.csv')

    lightcurve_visits_for_sn = {}
    for f in filters:
        lightcurve_visits_for_sn[f] = []
        dataIds = find_science_dataIds(f, repo_dir, dataset=dataset)
        # Restrict to first N, if requested
        if limit_n:
            # If limit_n > len(dataIds), that's fine.  [:limit_n] will just get the full array.
            dataIds = dataIds[:limit_n]

        if debug:
            print("DATA IDS: ", dataIds)
        for dataId in dataIds:
            lightcurve_visits_for_sn[f].append(dataId)
            if run_phot:
                run_forced_photometry(dataId, coord_file, repo_dir, dataset=dataset)
# How should this be done, and how should it be passed to assemble
    # We need to preserve order so that we read out the forced photometry
    # correctly later.
    lightcurve_visits = OrderedDict()
    for n in objects['Name']:
        lightcurve_visits[n] = lightcurve_visits_for_sn

    return lightcurve_visits


def run_photometry_for_objects(transient_objects, repo_dir, dataset='calexp',
                               filters=None, run_phot=True, limit_n=None,
                               verbose=False, debug=False):
    """Run photometry for given set of objects on all available images.

    run_phot : Run photometry.  If False then photometry is not run, but visits are gathered
    """
    # Can't put mutable as default argument above without much sadness.
    if filters is None:
        filters = ['J', 'H', 'K', 'KS']

    lightcurve_visits = {}
    for name, sn in transient_objects.items():
        coord_file = '{}_ra_dec.txt'.format(name)

        lightcurve_visits_for_sn = {}
        print("Processing photometry for {}".format(name))
        for f in filters:
            if verbose:
                print("FILTER: ", f)
                print(name, f, repo_dir, dataset)
            lightcurve_visits_for_sn[f] = []

            science_files = find_science_images(name, f, repo_dir, dataset=dataset, verbose=verbose)
            if verbose:
                print("Found science files:")
                print(find_science_images(name, f, repo_dir, dataset=dataset))

            dataIds = [{'fileroot': filename_to_fileroot(fn)} for fn in science_files]

            # Restrict to first N, if requested
            if limit_n:
                # If limit_n > len(dataIds), that's fine.  [:limit_n] will just get the full array.
                dataIds = dataIds[:limit_n]

            if debug:
                print("DATA IDS: ", dataIds)
            for dataId in dataIds:
                if run_phot:
                    try:
                        run_forced_photometry(dataId, coord_file, repo_dir, dataset=dataset)
                    except Exception as e:
                        print(e)
                        print("run-forced_photometry failed for {}".format(dataId))
                        continue
                lightcurve_visits_for_sn[f].append(dataId)

        lightcurve_visits[name] = lightcurve_visits_for_sn

    return lightcurve_visits


def parse_the_args():
    import argparse

    parser = argparse.ArgumentParser(description='Run catalog-based forced photometry')
    parser.add_argument('--dataset', default='calexp',
                        help='Dataset to photometry, e.g., "calexp" or "deepDiff_differenceExp"')
    parser.add_argument('--run_phot', default=True, action='store_true',
                        help='Run actual photometry.  Turn off for testing catalog assembly.')
    parser.add_argument('--no_run_phot', dest='run_phot', action='store_false')
    parser.add_argument('--limit_n', default=None, type=int,
                        help='Number of images per filter to analyze.')
    parser.add_argument('--repo_dir', default=repo_dir,
                        help='Butler repository to organize.')
    parser.add_argument('--verbose', default=False, action='store_true', help='Verbose output.')
    parser.add_argument('--debug', default=False, action='store_true', help='Debugging output.')

    return parser.parse_args()


def create_coord_file_from_diaSrc(dataId, repo_dir, out_file='coord_file.csv', dataset='deepDiff_diaSrc'):
    butler = dafPersist.Butler(repo_dir)
    diaSrc = butler.get(dataset, dataId=dataId, immediate=True)
    sources = Table([diaSrc['id'], np.rad2deg(diaSrc['coord_ra']), np.rad2deg(diaSrc['coord_dec'])],
                    names=('Name', 'RA', 'Dec'))
    sources.write(out_file)


def run(args):
    lightcurve_visits = run_photometry_for_objects(sn_with_dr1_templates, args.repo_dir, args.dataset,
                                                   limit_n=args.limit_n, run_phot=args.run_phot,
                                                   verbose=args.verbose, debug=args.debug)
    make_catalogs(lightcurve_visits, args.repo_dir, dataset=args.dataset)


if __name__ == "__main__":
    args = parse_the_args()
    run(args)
