#!/bin/bash
set -ef -o pipefail

# NOTE: need run_nwl_pkg.sh at least once to package examples

partis-nwl -v trace --find-links ./dist \
  --tool nwl_example.data_example \
  --inputs '' \
  --workdir tmp \
  --rundir data_run

partis-nwl -v trace --find-links ./dist \
  --tool nwl_example.grep \
  --inputs grep_inputs_query.yml \
  --workdir tmp \
  --rundir grep_run

partis-nwl -v trace --find-links ./dist \
  --tool nwl_example.module_example \
  --inputs '' \
  --workdir tmp \
  --rundir mod_run

partis-nwl -v trace --find-links ./dist \
  --tool nwl_example.generic \
  --inputs generic_inputs_query.yml \
  --workdir tmp \
  --rundir generic_run
