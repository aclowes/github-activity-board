#!/usr/bin/env bash

set -e

# clone if it doesn't exist
ls github-activity-board || git clone https://github.com/aclowes/github-activity-board.git

cd github-activity-board
git pull

pip install -q --upgrade pip setuptools
pip install -q requests google-cloud-storage

echo $GITHUB_ORGANIZATION
export PUBLIC_URL=/github-activity-board/$GITHUB_ORGANIZATION
yarn build
python github_report.py
python upload.py
