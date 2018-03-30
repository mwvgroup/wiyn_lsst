#!/usr/bin/env python

import glob
import os

import numpy as np

from astropy.io import fits
from astropy.table import Table

import esutil

import lsst.afw.geom
from lsst.afw.image import fluxFromABMag, fluxErrFromABMagErr
import lsst.afw.table as afwTable

DR1BASE = os.getenv('DR1BASE')


def get_2mass_test_file(dr1base=DR1BASE):
    """Return a sample photometry catalog from SweetSpot DR1 processing"""
    return "2MASS_LSQ13cwp.txt"


def get_dr1_test_file(dr1base=DR1BASE):
    """Return a sample photometry catalog from SweetSpot DR1 processing"""
    in_cat_dir = os.path.join(dr1base, 'catalogs')
    path_regex = os.path.join(in_cat_dir, 'LSQ13cwp*')

    cat_files = glob.glob(path_regex)

    test_file = cat_files[0]
    return test_file


def read_in_text_data(filename, debug=False):
    """Read in CSV file of catalog

    #RA DEC 2MASSID Jmag eJmag Hmag eHmag Kmag eKmag
    060.877901;-02.709703;04033069-0242349 ;13.922; 0.028;13.449; 0.032;13.303; 0.038
    060.921678;-02.695895;04034120-0241452 ;14.831; 0.035;14.174; 0.037;13.975; 0.054
    060.903753;-02.706162;04033690-0242221 ;15.905; 0.082;15.553; 0.114;15.226; 0.152
    """
    colnames = ('RA', 'DEC', '2MASSID',
                'Jmag', 'eJmag', 'Hmag', 'eHmag', 'Kmag', 'eKmag')
    data = Table.read(filename, format='csv', delimiter=';', data_start=1, names=colnames)
    if debug:
        print(data)

    return data


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


def twomass_int_id(str_id):
    """Compute a pure integer representation of 2MASS ID

    Map '-', '+' to 0, 1

    >>> compute_2mass_int_id('04033069-0242349')
    403306900242349
    >>> compute_2mass_int_id('2MASS04033069-0242349')
    403306900242349
    >>> compute_2mass_int_id('2MASS04033069+0242349')
    403306910242349
    """
    ra_length = 8
    dec_length = 7
    id_length = ra_length + 1 + dec_length
    # Do lookup from back to work whether or not there's a prefix of
    # '2MASS' or '2MASS '
    ra_str = str_id[-id_length:-(1 + dec_length)]
    sign_str = str_id[-(1+dec_length):-dec_length]
    dec_str = str_id[-dec_length:]
    # Keep as string for composition later
    if sign_str == '-':
        sign_str_as_int = '0'
    elif sign_str == '+':
        sign_str_as_int = '1'
    else:
        print('BAD CONFUSING THINGS WITH PARSING of 2MASS ID:', str_id)

    id_str = ra_str + sign_str_as_int + dec_str
    return int(id_str)


def vegaToABMag(vega_mag, filt):
    """Convert Vega magnitude to AB Magnitude for given filter.

    Supported filters are 'J', 'H', 'Ks'
      http://www.astronomy.ohio-state.edu/~martini/usefuldata.html
    Blanton and Roweis, 2007, AJ, 133, 734.
      http://adsabs.harvard.edu/abs/2007AJ....133..734B
    """
    mAB_minus_mVega = {'J': 0.91, 'H': 1.39, 'Ks': 1.85}
    return vega_mag + mAB_minus_mVega[filt]


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
    for row in out_table:
        record = out_cat.addNew()
        record.setId(twomass_int_id(row['2MASSID']))
        record.setRa(float(row['coord_ra']) * lsst.afw.geom.degrees)
        record.setDec(float(row['coord_dec']) * lsst.afw.geom.degrees)
        abMag = vegaToABMag(row[filtMag], filt)  # error remains unchanged
        record.set(filtFlux, fluxFromABMag(abMag))
        record.set(filtFluxSigma, fluxErrFromABMagErr(row[filtMagSigma], abMag))

    return out_cat


def convert_2mass_to_output_data(data, debug=False):
    """Convert from 2MASS catalog -> afw Table Source catalog

    Parameters
    --
    data : astropy.table.Table

    Return
    --
    out_table : afw Source table.

    """
    out_table = data.copy()

    translate = {'coord_ra': 'RA', 'coord_dec': 'DEC'}
    filters = ('J', 'H', 'K')
    for f in filters:
        old_mag, old_mag_err = '%smag' % f, 'e%smag' %f
        new_mag, new_mag_err = '%s_mag' % f, '%s_mag_sigma' %f
        translate[new_mag] = old_mag
        translate[new_mag_err] = old_mag_err

    for new_name, old_name in translate.items():
        out_table.rename_column(old_name, new_name)

    out_cat = make_source_catalog_from_astropy_table(out_table, debug=debug)

    return out_cat


def convert_dr1_to_output_data(data, debug=False):
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
    ids = h.lookup_id(data['RA'], data['DEC'])
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
    test_file = get_2mass_test_file()
    convert_cat_to_htm(test_file, debug=debug)


def convert_cat_to_htm(filename, debug=False):
    """Convert the catalog given by filename into an HTM-sharded AFW catalog.
    """
    data = read_in_text_data(filename)
    shard_ids, sharded_data = shard_data(data, debug=debug)

    write_master_schema(sharded_data[0])

    for id, sd in zip(shard_ids, sharded_data):
        out_data = convert_2mass_to_output_data(sd, debug=debug)
        write_out_data(out_data, id=id)


def get_2mass_catalog_files(dr1base=DR1BASE):
    """Return the full filenames of files in DR1BASE/2MASS_catalogs"""
    return glob.glob(os.path.join(dr1base, "2MASS_catalogs", "*.txt"))


def process_dr1_2mass_cat_to_html(dr1base=DR1BASE, debug=False):
    """Iterate through the 80 DR1 fields

    74 SNeIa + 6 Persson standard star fields

    Assume that no shard covers two separate fields
    so that we can just iterate through fields and generate the shards for each.
    """
    catalog_files = get_2mass_catalog_files(dr1base=DR1BASE)
    for cf in catalog_files:
        convert_cat_to_htm(cf, debug=debug)


if __name__ == "__main__":
    debug = True
    test_example_catalog(debug=debug)
