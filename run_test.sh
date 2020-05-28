#!/bin/sh
sudo -u postgres dropdb capstone_test
sudo -u postgres createdb capstone_test
sudo -u postgres psql capstone_test < capstone.psql