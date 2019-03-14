#!/bin/sh

python3 main.py --model_save_path "./model_weights_directory" \
--lr 1e-4 \
--batch_size 128 \
--epochs 1e6 \
--optimizer "adam" \
--metric "val_loss" \
-v \