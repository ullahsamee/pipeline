#!/bin/bash

docker run -it --gpus all --name dl_binder_container -v /home/btb/karl/dl_binder_design:/app/data dl_binder_design bash
