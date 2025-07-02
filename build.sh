#!/bin/bash
mkdir -p base-files
cp -rf etc DEBIAN usr base-files
cd base-files
mkdir bin  boot  dev  etc  home  lib  proc  root  run  sbin  sys  tmp
mkdir -p var/{backups,cache,lib/{dpkg,misc},local,lock,log,run,spool,tmp}
cd ..
python3 base_file_pack_unpack.py