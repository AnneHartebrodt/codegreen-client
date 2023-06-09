#!/usr/bin/env bash

echo $(which python)
 
conda init bash

source ~/.bashrc

conda activate greenerai-client

python /home/bionets-og86asub/Documents/greenerai/greenerai-client/src/nextflow_adapter.py
