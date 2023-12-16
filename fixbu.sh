#!/bin/bash

for db in ./*; do
    if [ -d "$db" ]; then
        for coll in "$db"/*; do
            if [ -d "$coll" ]; then
                mv "$coll"/* "$coll"/..
                rmdir "$coll"
            fi
        done
    fi
done

