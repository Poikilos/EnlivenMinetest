#!/bin/bash
cd /opt
if [ $? -ne 0 ]; then
    exit 1
fi
source lmk.rc
if [ $? -ne 0 ]; then
    exit 1
fi
