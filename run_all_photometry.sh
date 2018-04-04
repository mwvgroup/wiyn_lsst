#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

bash run_photometry.sh "${REPO}" LSQ13cwp
bash run_photometry.sh "${REPO}" PTF11mty
