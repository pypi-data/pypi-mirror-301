#!/bin/bash
set -ef -o pipefail

partis-nwl-pkg -v trace --no-doc --out ./dist pkg_nwl_example.yml

partis-nwl-pkg -v trace --no-doc --out ./dist pkg_mpi_example.yml
