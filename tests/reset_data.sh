#!/bin/bash

# Used to reset tests/data to data-copy

rm -rf data
mkdir data
cp -r data-copy/* data/.