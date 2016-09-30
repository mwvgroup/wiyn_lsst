#!/bin/bash

WIYN=${HOME}/tmp
REPO=${WIYN}/test_dr1

fileroot=SN2011gy_A_H_20111115
coord_file=SN2011gy_ra_dec.txt

# Single epoch science stack
python forcedPhotExternalCatalog.py "${REPO}" --output "${REPO}" --id fileroot="${fileroot}" --coord_file "${coord_file}" --clobber-versions
# Subtraction
#  Should add a dataset option or something to select 'diffim' instead of 'exposure'
python forcedPhotExternalCatalog.py "${REPO}" --output "${REPO}" --id fileroot="${fileroot}" --coord_file "${coord_file}" --clobber-versions
