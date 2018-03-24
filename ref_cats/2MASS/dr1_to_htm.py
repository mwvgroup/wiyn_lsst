#!/usr/bin/env python

import glob
import os

import numpy as np

from astropy.io import fits
from astropy.table import Table

in_cat_dir = os.path.join(os.getenv('DR1BASE'), 'catalogs')
path_regex = os.path.join(in_cat_dir, 'LSQ13cwp*')

cat_files = glob.glob(path_regex)

test_file = cat_files[0]
# Read in
data = fits.getdata(test_file)
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
for new_name, old_name in translate.items():
    out_table.rename_column(old_name, new_name)

# [Divide in HTM]
# Write out
out_table.write('test_out.fits', overwrite=True)
