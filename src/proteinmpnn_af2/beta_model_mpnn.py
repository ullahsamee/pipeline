#!/bin/bash
rm check.point 2>/dev/null
/app/mpnn_fr/dl_interface_design.py -pdbdir /app/data/input/pdbs -relax_cycles 0 -seqs_per_struct 4 -outpdbdir /app/data/output
