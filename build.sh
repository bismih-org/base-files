#!/bin/bash

rm -rf build
mkdir build
cp -r bin  boot  DEBIAN  dev  etc  home  LICENSE  lib  proc  root  run  sbin  sys  tmp  usr  var build/

cd build

dpkg-deb --build . ../base-files_12.4+z-bismih24.2.1_all.deb