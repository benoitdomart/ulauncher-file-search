#!/bin/bash

for i in $(find /home/ben/Documents/Cours/2025-2026 -iname '*ts*' ); 
do
    $DIR=`$(dirname ${i})`
    echo $DIR
done


find /home/ben/Documents/Cours/2025-2026 -iname *aide*linux* | sed 's|^/[^/]*/[^/]*/[^/]*/[^/]*/||'