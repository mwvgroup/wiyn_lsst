#!/usr/bin/env python

"""
Take an input text file of RA, Dec
Write out a SourceCatalog
Use SourceCatalog and forcePhotDiaSources.py to extract photometry
  https://github.com/lsst-dm/dmtn-006/blob/master/python/forcePhotDiaSources.py
"""

import os

from astropy.table import Table

from lsst.afw.table import SourceCatalog, SchemaMapper, Field
import lsst.daf.persistence as dafPersistence

from lsst.afw.geom import Angle, AngleUnit, degrees

from lsst.meas.base.forcedMeasurement import forcedMeasurementTask

# def test_create_source_catalog_from_text_and_butler():
# k    create_source_catalog_from_text_and_butler()

def measure_photometry_from_source_catalog(repo_dir, src_cat):
    butler = dafPersistence.Butler()

    exposure = butler.get("calexp", dataId=diaSourceRef.dataId)
    refWcs = exposure.getWcs()

    refCat =  butler.get() #self.fetchReferences(exposure)
    measCat = self.measurement.generateMeasCat(exposure, refCat, refWcs)

    #self.log.info("Performing forced measurement on science image %s" % scienceExpRef.dataId)

    self.measurement.attachTransformedFootprints(measCat, refCat, exposure, refWcs)
    self.measurement.run(measCat, exposure, refCat, refWcs)


def create_source_catalog_from_text_and_butler(repo_dir, info, dataset='src'):
    butler = dafPersistence.Butler(repo_dir)
    schema = butler.get(dataset + "_schema", immediate=True).schema
    mapper = SchemaMapper(schema)
    mapper.addMinimalSchema(schema)
    newSchema = mapper.getOutputSchema()

    src_cat = SourceCatalog(newSchema)
    for row in info:
        record = src_cat.addNew()
        record.set('coord_ra', Angle(row['RA']*degrees))
        record.set('coord_dec', Angle(row['Dec']*degrees))

    print(src_cat['coord_ra'], src_cat['coord_dec'])
    return(src_cat)


def writeOutput(self, dataRef, sources):
    """Write forced source table

    @param dataRef  Data reference from butler; the forced_src dataset (with self.dataPrefix included)
                    is all that will be modified.
    @param sources  SourceCatalog to save
    """
    dataRef.put(sources, self.dataPrefix + "forced_src") 


if __name__ == "__main__":
    sn_coord_file = 'SN2011gy_ra_dec.txt'
    info = Table.read(sn_coord_file, format='ascii.csv', names=('Name', 'RA', 'Dec'))

    repo_dir = os.path.join(os.getenv('HOME'), 'tmp', 'test_dr1')
    src_cat = create_source_catalog_from_text_and_butler(repo_dir, info)
    measure_photometry_from_source_catalog(src_cat)

