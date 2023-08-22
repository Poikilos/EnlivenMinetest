#!/bin/bash
found=false
# LD_LIBRARY_PATH=/usr/lib64
# export LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/lib64
for try_dir in ../git/EnlivenMinetest/utilities .
do
    if [ -f $try_dir/run-any ]; then
        if [ "x$found" != "xtrue" ]; then
            found=true
            echo "[run-any.sh] Found $try_dir..."
            $try_dir/run-any "$@"
            if [ $? -ne 0 ]; then
                echo "[run-any.sh] the command failed in \"`pwd`\". Tried:"
                echo "[run-any.sh] $try_dir/run-any"
                echo "with args:"
                for arg in $@
                do
                    echo "$arg"
                    if [ ! -f "$arg" ]; then
                        echo "(not in \"`pwd`\")"
                    fi
                done
            fi
        fi
    else
        echo "There is no `realpath $try_dir/run-any`"
    fi
done
if [ "x$found" != "xtrue" ]; then
    echo "File $0, line 3: run-any was not found from working dir \"`pwd`\"."
    echo "  The vscode project using this file should set cwd or path to something like /home/user/minetest"
    exit 1
fi
