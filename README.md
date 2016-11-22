Processing of SweetSpot WIYN images using LSST DM Stack.

Requires the definition of the environment variable DR1BASE and the existence of SweetSpot stacks in ${DR1BASE}/stacks.

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
