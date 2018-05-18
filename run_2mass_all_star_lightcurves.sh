#!/bin/bash

# Extrat the Field, 2MASS calibration star for the DR1 analysis
# Format to run sn_lightcurve.py

# ls ${DR1BASE}/lightcurves/ | cut -f 1 -d \. | awk -F _ '{print $1, $2}' | grep 2MASS > dr1_2mass_stars.dat
file=dr1_2mass_stars.dat

grep -v \# ${file} | awk '{printf "%s ", $1}' > field.list
grep -v \# ${file} | awk '{printf "%s ", $2}' > 2mass_star.list

python sn_lightcurve.py `cat field.list` --target `cat 2mass_star.list`
