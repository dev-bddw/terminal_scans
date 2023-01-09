#! /bin/sh

sudo docker-compose -f local.yml run --rm django coverage run -m pytest
