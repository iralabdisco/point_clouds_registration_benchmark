#!/bin/bash

global_file=$1

for file in *.pcd;
do
    echo $file
    if ! grep -q $file $global_file;
    then
        rm $file
    fi
done