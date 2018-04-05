#config.doPreConvolve=False
#config.doMatchSources=False
#config.doAddMetrics=False
config.doUseRegister=False
config.convolveTemplate=True
#config.doSelectSources=False
#config.kernelSourcesFromRef=False
config.doWriteMatchedExp=True
config.doDecorrelation=True

from lsst.ip.diffim.getTemplate import GetCalexpAsTemplateTask
config.getTemplate.retarget(GetCalexpAsTemplateTask)
