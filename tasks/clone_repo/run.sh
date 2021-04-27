#!/bin/bash

cd /data/projects

if [ -d ./car-insurance-ssh ]; then
  cd car-insurance-ssh

  git pull origin master
else
  git clone git@github.com:Therealchainman/car-insurance.git car-insurance-ssh
  cd car-insurance-ssh
fi

git config user.email "${EMAIL}"
git config user.name "${USER}"
