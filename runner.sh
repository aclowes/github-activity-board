#!/usr/bin/env bash

set -e

# clone if it doesn't exist
ls github-activity-board || git clone https://github.com/aclowes/github-activity-board.git

cd github-activity-board
git pull

pip install -q --upgrade pip setuptools
pip install -q requests google-cloud-storage

# install nodejs and yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

curl -sS https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
echo "deb https://deb.nodesource.com/node_8.x jessie main" | tee /etc/apt/sources.list.d/nodesource.list

apt-get install -q -y apt-transport-https
apt-get update -q
apt-get install -q -y nodejs yarn

# calculate activity
echo $GITHUB_ORGANIZATION
export PUBLIC_URL=/github-activity-board/$GITHUB_ORGANIZATION
yarn build
python github_report.py
python upload.py
