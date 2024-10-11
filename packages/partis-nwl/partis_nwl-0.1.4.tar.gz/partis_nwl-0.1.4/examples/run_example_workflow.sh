#!/bin/bash
set -ef -o pipefail

# NOTE: need run_nwl_pkg.sh at least once to package examples
partis-nwl -v info --find-links ./dist \
  --workdir tmp \
  example_workflow.yml
