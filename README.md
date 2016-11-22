Processing of SweetSpot WIYN images using LSST DM Stack.

Requires the definition of the environment variable DR1BASE and the existence of SweetSpot stacks in ${DR1BASE}/stacks.

### Run the following to process
1. Create LSST-formatted FITS with image, weight map, and mask.
`sh make_wiyn_dr1_lsst.sh`
2. Ingest files
`sh ingest_wiyn_dr1_images.sh`
3. processCcd files
`sh run_wiyn.sh`
4. Run subtractions
`python sub_wiyn_dr1.py`
5. Make coord files
`sh make_coord_files.sh`
6. Run lightcurves on subtractions
`python wiyn_forcedPhotExternalCatalog.py`

Notes:
1. Coord files are used in assemble catalogs, but not run_forced_photometry_per_object. should make consistent.

### Batch queue processing (SLURM)
The simplest job would just be to run the above commands in a single-node, serial job.

The slightly more efficient job spreads out the processing of the processCcd step, which is the the most expensive step.

3. processCcd
`sbatch run_processCcd_each_field_jobarray.sl`
4. Run subtractions
`sbatch run_subtractions.sl`
5. Run lightcurves
`sbatch run_forced_photometry.sl`
