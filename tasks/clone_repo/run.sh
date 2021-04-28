#!/bin/bash

cd /data/projects

if [ -d ./motion_prediction]; then
  cd motion_prediction

  git pull origin master
else
  git clone git@github.com:Therealchainman/motion_prediction.git motion_prediction
  cd motion_prediction
fi

git config user.email "${EMAIL}"
git config user.name "${USER}"
