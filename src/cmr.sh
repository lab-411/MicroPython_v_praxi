#!/bin/bash
# compile 
./cmc.sh $1
# view
sxiv $(basename $1 .ckt).png &
