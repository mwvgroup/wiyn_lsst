#!/usr/bin/env python

import glob
import os

import numpy as np

from astropy.io import fits
from astropy.table import Table

import esutil

import lsst.afw.geom
import lsst.afw.table as afwTable

DR1BASE = os.getenv('DR1BASE')

def get_test_file(dr1base=DR1BASE):
    """Return a sample photometry catalog from SweetSpot DR1 processing"""
    in_cat_dir = os.path.join(dr1base, 'catalogs')
    path_regex = os.path.join(in_cat_dir, 'LSQ13cwp*')

    cat_files = glob.glob(path_regex)

    test_file = cat_files[0]
    return test_file


def read_in_data(test_file, remove_last_row=True):
    """Read in test_file as a binary table FITS file.

    Parameters
    --
    test_file : Full path of input catalog name
    remove_last_row : Remove the last row of the catalog.
        The DR1 catalogs have the SN as the last row of the forced photometry
        We don't want this for the calibration catalogs so by default
        we remove this line.
    """
    data = fits.getdata(test_file)
    # Remove last row, which is the SN
    if remove_last_row:
        data = data[:-1]

    return data


def makeMinimalSchema(filt=None, debug=False):
    """Make a minimal schema """

    schema = afwTable.SourceTable.makeMinimalSchema()
    schema.addField(
        field="%s_flux" % filt,
        type=np.float64,
        doc="%s flux" % filt,
    )
    schema.addField(
        field="%s_fluxSigma" % filt,
        type=np.float64,
        doc="%s flux uncertainty" % filt,
    )
    if debug:
        print("SCHEMA: ")
        print(schema)

    return schema


def make_source_catalog_from_astropy_table(out_table, debug=False):
    """Return an AFW SourceCatalog from an Astropy Table

    Written with extensive reference to
    https://github.com/lsst/meas_astrom/blob/master/convertToFitsTable.py
    """
    filt = 'H'
    schema = makeMinimalSchema(filt=filt, debug=debug)
    out_cat = afwTable.SourceCatalog(schema)

#    psfFluxKey = schema.getKey('psfFlux')
#    psfFluxKeySigma = schema.getKey('psfFluxSigma')
    filt = 'H'
    filtMag = '%s_mag' % filt
    filtMagSigma = '%s_mag_sigma' % filt
    filtFlux = '%s_flux' % filt
    filtFluxSigma = '%s_fluxSigma' % filt
    for i, row in enumerate(out_table):
        record = out_cat.addNew()
        record.setId(int(i))  # Use this enumerator instead of the 2MASS ID string
        record.setRa(float(row['coord_ra']) * lsst.afw.geom.degrees)
        record.setDec(float(row['coord_dec']) * lsst.afw.geom.degrees)
        record.set(filtFlux, float(row[filtMag]))
        record.set(filtFluxSigma, float(row[filtMagSigma]))

    return out_cat


def convert_to_output_data(data, debug=False):
    """Convert from DR1 FITS -> afw Table Source catalog

    Return
    --
    out_table : afw Source table.

    """
    in_table = Table(data)

    # Reformat
    filt = 'H'
    translate = {'coord_ra': 'RA', 'coord_dec': 'DEC',
                '%s_mag' % filt: 'CAL_MAG',
                '%s_mag_sigma' % filt: 'CAL_MAG_ERR'}

    reverse_translate = {v: k for k, v in translate.items()}

    values = [v for v in translate.values()]
    # out_data =

    ref_cat_entries = np.isfinite(in_table['CAL_MAG'])
    out_table = in_table[ref_cat_entries]

    for new_name, old_name in translate.items():
        out_table.rename_column(old_name, new_name)

    out_cat = make_source_catalog_from_astropy_table(out_table, debug=debug)

    return out_cat
#    return out_table


def write_master_schema(out_table, debug=False):
    filt = 'H'
    schema = makeMinimalSchema(filt=filt, debug=debug)
    master_schema = afwTable.SourceCatalog(schema)

    master_schema.writeFits('master_schema.fits')


def write_out_data(out_table, id=0, debug=False):
    out_table.writeFits('%06d.fits' % id)


def shard_data(data, depth=7, debug=False):
    """Divide input AstroPy table into list of tables by HTM shards

    Parameters
    --
    data : AstroPy table

    Returns
    --
    [shard1, shard2, ...]  List of AstroPy tables divided by HTM shard.
    """
    h = esutil.htm.HTM(depth=7)
    # Implicitly Assume ICRS:  HTM doesn't directly care, it's just doing
    # spherical geometry.  But we're assuming here that we're using the same
    # RA, Dec convention that will be used in the LSST code , which is ICRS.
    ids = h.lookup_id(data['RA'], data['Dec'])
    uniq_ids = np.unique(ids)
    if debug:
        print('IDS: ', ids)
        print('UNIQ_IDS: ', uniq_ids)
    # Keep the simple case simple
    if uniq_ids == 1:
        return [data]

    data_list = []
    for id in uniq_ids:
        w, = np.where(ids == id)
        these_data = data[w]
        data_list.append(these_data)

    return uniq_ids, data_list


def test_example_catalog(debug=False):
    test_file = get_test_file()
    data = read_in_data(test_file)
    shard_ids, sharded_data = shard_data(data, debug=debug)

    write_master_schema(sharded_data[0])

    for id, sd in zip(shard_ids, sharded_data):
        out_data = convert_to_output_data(sd, debug=debug)
        write_out_data(out_data, id=id)


if __name__ == "__main__":
    debug = True
    test_example_catalog(debug=debug)
