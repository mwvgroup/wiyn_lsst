#!/usr/bin/env python

from __future__ import print_function, division

import lsst
import lsst.meas.base as measBase
import lsst.afw.table as afwTable
import lsst.pipe.base as pipeBase
from lsst.afw.geom import Angle, degrees


class TaskRunnerWithArgs(pipeBase.ButlerInitializedTaskRunner):
    """Overwrite default TaskRunner to pass 'coord_file' in the kwargs dict to 'run'"""
    @staticmethod
    def getTargetList(parsedCmd, **kwargs):
        return pipeBase.TaskRunner.getTargetList(parsedCmd,
                                                 coord_file=parsedCmd.coord_file,
                                                 **kwargs)


def load_external_catalog_info(coord_file):
    """Load name, ra, dec information from an external csv catalog.

    >>> tmpfile = 'foo.csv'
    >>> with open(tmpfile, 'w') as f:
    ...     f.write("Name,RA,Dec\\n")
    ...     f.write("SN2011gy,52.397163,40.867481")
    >>> foo = load_external_catalog_info(tmpfile)
    >>> print(foo)  # doctest: +NORMALIZE_WHITESPACE
      Name       RA       Dec
    -------- --------- ---------
    SN2011gy 52.397163 40.867481

    """
    from astropy.table import Table

    info = Table.read(coord_file, format='ascii.csv', names=('Name', 'RA', 'Dec'))
    return info


class ForcedPhotExternalCatalogConfig(lsst.pex.config.Config):
    """Config class for forced measurement driver task."""

    measurement = lsst.pex.config.ConfigurableField(
        target=measBase.ForcedMeasurementTask,
        doc="subtask to do forced measurement")

    def setDefaults(self):
        # RaDecCentroid takes the centroid from the reference catalog and uses it.
        self.measurement.plugins.names = ["base_RaDecCentroid", "base_PsfFlux"]
        self.measurement.slots.shape = None
        self.measurement.slots.centroid = "base_RaDecCentroid"


class ForcedPhotExternalCatalogTask(pipeBase.CmdLineTask):

    ConfigClass = ForcedPhotExternalCatalogConfig
    RunnerClass = TaskRunnerWithArgs
    _DefaultName = "ForcedPhotExternalCatalogTask"

    def __init__(self, butler=None, **kwargs):
        super(lsst.pipe.base.CmdLineTask, self).__init__(**kwargs)

        # We need an example output table from measurement to load.
        dataset = 'src'
        self.refSchema = butler.get(dataset + "_schema", immediate=True).schema
        self.makeSubtask("measurement", refSchema=self.refSchema)
        self.dataPrefix = ""

    def create_source_catalog_from_external_catalog(self, dataRef, coord_file, dataset='src', debug=True):
        butler = dataRef.getButler()
        schema = butler.get(dataset + "_schema", immediate=True).schema
        mapper = afwTable.SchemaMapper(schema)
        mapper.addMinimalSchema(schema)
        newSchema = mapper.getOutputSchema()

        info = load_external_catalog_info(coord_file)

        src_cat = afwTable.SourceCatalog(newSchema)
        for row in info:
            record = src_cat.addNew()
            record.set('coord_ra', Angle(row['RA']*degrees))
            record.set('coord_dec', Angle(row['Dec']*degrees))

        if debug:
            print(src_cat['coord_ra'], src_cat['coord_dec'])
        return(src_cat)

    def run(self, dataRef, coord_file=None):
        """ Perform forced photometry on the dataRef exposure at the locations in coord_file.
        """

        butler = dataRef.getButler()
        exposure = butler.get("calexp", dataId=dataRef.dataId)
        refWcs = exposure.getWcs()

        refCat = self.create_source_catalog_from_external_catalog(dataRef, coord_file)

        measCat = self.measurement.generateMeasCat(exposure, refCat, refWcs)

        # self.log.info("Performing forced measurement on science image %s" % scienceExpRef.dataId)

        self.measurement.attachTransformedFootprints(measCat, refCat, exposure, refWcs)
        self.measurement.run(measCat, exposure, refCat, refWcs)

        self.writeOutput(dataRef, measCat)

    def writeOutput(self, dataRef, sources):
        """!Write forced source table
        @param dataRef  Data reference from butler; the forced_src dataset (with self.dataPrefix included)
                        is all that will be modified.
        @param sources  SourceCatalog to save
        """
        dataRef.put(sources, self.dataPrefix + "forced_src")

    @classmethod
    def _makeArgumentParser(cls):
        parser = lsst.pipe.base.ArgumentParser(name=cls._DefaultName)

        # Can I make an argument which is a dataset type?
        parser.add_id_argument("--id", "src", help="data ID of the image")
        parser.add_argument("--coord_file",
                            help="File with coordinates to photometry. " +
                            "Each line should be Name,RA,Dec with RA, Dec as decimal degrees.")
        return parser

    # Overriding these two functions prevent the task from attempting to save the config.
    def _getConfigName(self):
        return None

    def _getMetadataName(self):
        return None


if __name__ == "__main__":

    ForcedPhotExternalCatalogTask.parseAndRun()
