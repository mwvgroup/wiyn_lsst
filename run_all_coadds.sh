#!/bin/bash

WIYN=${DR1BASE}/tmp
REPO=${WIYN}/test_dr1

bash run_coadd.sh "${REPO}" LSQ13cwp 0 20131111 521
bash run_coadd.sh "${REPO}" PTF11mty 1 20111025 218
