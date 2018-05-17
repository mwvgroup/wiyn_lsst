#!/bin/bash

# Extrat the Field, 2MASS calibration star for the DR1 analysis
# Format to run sn_lightcurve.py

file=dr1_cal_stars.dat

grep -v \# ${file} | awk '{printf "%s ", $1}' > sn.list
grep -v \# ${file} | awk '{printf "%s ", $2}' > cal_star.list

python sn_lightcurve.py `cat sn.list` --target `cat cal_star.list`
