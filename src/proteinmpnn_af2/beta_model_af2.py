#!/bin/bash
rm check.point 2>/dev/null
/app/af2_initial_guess/predict.py -pdbdir /app/data/input/mpnn_output -outpdbdir /app/data/af2_output
