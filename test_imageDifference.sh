#!/bin/bash

imageDifference.py ~/tmp/test_dr1 --id fileroot=SN2011gy_A_H_20111115  --templateId fileroot=SN2011gy_A_H_20121028 --output ~/tmp/test_dr1 --configfile diffimconfig.py --logdest wiyn_imageDifference.log --clobber-config --clobber-versions
imageDifference.py ~/tmp/test_dr1 --id fileroot=SN2011gy_A_H_20111121  --templateId fileroot=SN2011gy_A_H_20121028 --output ~/tmp/test_dr1 --configfile diffimconfig.py --logdest wiyn_imageDifference.log --clobber-config --clobber-versions
imageDifference.py ~/tmp/test_dr1 --id fileroot=SN2011gy_A_H_20120108  --templateId fileroot=SN2011gy_A_H_20121028 --output ~/tmp/test_dr1 --configfile diffimconfig.py --logdest wiyn_imageDifference.log --clobber-config --clobber-versions
