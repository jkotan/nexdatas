#!/usr/bin/env bash

echo "run python-nxswriter"
docker exec -it ndts python test/runtest.py 
if [ $? -ne "0" ]
then
    exit -1
fi
