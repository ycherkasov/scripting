#!/bin/bash
cd /usr/bin
rm cc gcc c++ g++
#mv ld ld.bak
ln -s /usr/local/bin/gcc-4.9 cc
ln -s /usr/local/bin/gcc-4.9 gcc
ln -s /usr/local/bin/c++-4.9 c++
ln -s /usr/local/bin/g++-4.9 g++
#ln -s /usr/local/bin/gcc-4.9 ld