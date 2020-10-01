#!/bin/bash
cd /usr/bin
rm cc gcc c++ g++
#cp ld.bak ld
ln -s /usr/bin/clang cc
ln -s /usr/bin/clang gcc
ln -s /usr/bin/clang++ c++
ln -s /usr/bin/clang++ g++
