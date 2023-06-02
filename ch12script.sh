##!/bin/bash

## Part one
cat ./deploy_tools/nginx.template.conf \
    | sed "s/DOMAIN/claireville.crabdance.com/g" \
    | tee /etc/nginx/sites-available/claireville.crabdance.com

## Part two
ln -s /etc/nginx/sites-available/claireville.crabdance.com \
    /etc/nginx/sites-enabled/claireville.crabdance.com

## Part three
cat ./deploy_tools/claireville.crabdance.com.template.service \
    | sed "s/DOMAIN/claireville.crabdance.com/g" \
    |  tee /etc/systemd/system/claireville.crabdance.com.service


