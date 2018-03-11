#!/bin/bash -l

#SBATCH -p shared  
#SBATCH -n 4
#SBATCH --mem=8GB
#SBATCH -t 02:00:00     
#SBATCH -J wiynsub
#SBATCH -L project
#SBATCH -C haswell

export OMP_NUM_THREADS=4

# Set up LSST environment for WIYN+WHIC
# LSST Stack Conda installed maintained by Heather Kelly

# Twinkles Hack Weeek version
source /global/common/cori/contrib/lsst/lsstDM/setupStack-12_1.sh

# obs_lsstSim 12.1 + one commit
setup -j -r /global/homes/w/wmwv/local/lsst/obs_file
setup -j -r /global/homes/w/wmwv/local/lsst/meas_base

# Overwrite the catalog location to get the 2MASS catalogs.
export ASTROMETRY_NET_DATA_DIR=/project/projectdirs/m1727/cat/2MASS

# WIYN=${HOME}/tmp
WIYN=/global/project/projectdirs/lsst/wmwv/test/
REPO=${WIYN}/test_dr1

python sub_wiyn_dr1.py ${REPO}
