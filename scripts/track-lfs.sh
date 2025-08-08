#!/bin/bash

# run it in workspace directory only not in /scripts

cd "$(dirname "$0")/.."

mkdir -p ./notebooks/data
git lfs track ./notebooks/data/*.*


mkdir -p ./artifacts
git lfs track ./artifacts/*.*