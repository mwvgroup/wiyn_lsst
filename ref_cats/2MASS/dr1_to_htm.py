#!/usr/bin/env python

import glob
import os

import numpy as np

from astropy.io import fits
from astropy.table import Table

import lsst.afw.table as afwTable

DR1BASE = os.getenv('DR1BASE')

def get_test_file(dr1base=DR1BASE):
    """Return a sample photometry catalog from SweetSpot DR1 processing"""
    in_cat_dir = os.path.join(dr1base, 'catalogs')
    path_regex = os.path.join(in_cat_dir, 'LSQ13cwp*')

    cat_files = glob.glob(path_regex)

    test_file = cat_files[0]
    return test_file


def read_in_data(test_file):
    """Read in test_file as a binary table FITS file."""
    return fits.getdata(test_file)


def makeMinimalSchema(filter=None, debug=False):
    """Make a minimal schema """

    schema = afwTable.SourceTable.makeMinimalSchema()
    schema.addField(
        field="%s_mag" % filter,
        type=np.float64,
        doc="%s magnitude" % filter,
    )
    schema.addField(
        field="%s_mag_sigma" % filter,
        type=np.float64,
        doc="%s magnitude uncertainty" % filter,
    )
    if debug:
        print("SCHEMA: ")
        print(schema)

    return schema


def convert_to_output_data(data):
    """Convert from DR1 FITS -> afw Table Source catalog

    Return
    --
    out_table : afw Source table.

    """
    in_table = Table(data)

    # Reformat
    filter = 'H'
    translate = {'coord_ra': 'RA', 'coord_dec': 'DEC',
                 '%s_mag' % filter: 'CAL_MAG'}

    reverse_translate = {v: k for k, v in translate.items()}

    values = [v for v in translate.values()]
    # out_data =

    ref_cat_entries = np.isfinite(in_table['CAL_MAG'])
    out_table = in_table[ref_cat_entries]

    schema = makeMinimalSchema(filter=filter)
    out_cat = afwTable.SourceCatalog(schema)

    for new_name, old_name in translate.items():
        out_table.rename_column(old_name, new_name)

    return out_table


def write_master_schema(out_table):
    # This is silly.  Should directly copy metadata.
    master_schema = out_table.copy()
    master_schema.remove_rows(slice(0, len(master_schema)))
    master_schema.write('master_schema.fits', overwrite=True)


def write_out_data(out_table):
    # [Divide in HTM]
    # Write out
    out_table.write('test_out.fits', overwrite=True)


def test_example_catalog():
    test_file = get_test_file()
    data = read_in_data(test_file)
    out_data = convert_to_output_data(data)
    write_out_data(out_data)
    write_master_schema(out_data)


if __name__ == "__main__":
    test_example_catalog()
