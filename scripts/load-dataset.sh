#!/bin/bash

# run it in workspace directory only not in /scripts

cd "$(dirname "$0")/.."

mkdir -p ./notebooks/data
curl -L -o ./notebooks/data/sms-spam-collection-dataset.zip\
  https://www.kaggle.com/api/v1/datasets/download/uciml/sms-spam-collection-dataset


# unzip
unzip -o ./notebooks/data/sms-spam-collection-dataset.zip -d ./notebooks/data/

# remove zip
rm -f ./notebooks/data/sms-spam-collection-dataset.zip