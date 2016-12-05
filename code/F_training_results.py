#!/usr/bin/env python
#coding=utf-8
import os
import json

FILENAME = "R_training_results.json"

def get_threshold(var):
    return 0.05 * int(var.split("/")[0])

def get_analysis(var):
    var = var.split("/")[-1]
    var = var.replace("D_training_", "")
    var = var.split("-")[0]
    return var

def get_method(var):
    return var.split("/")[1]

if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        raise IOError('Unable to find: %s' % FILENAME)
    
    with open(FILENAME, 'r') as handle:
        content = json.load(handle)
    
    with open(FILENAME.replace(".json", '.txt'), 'w') as handle:
        for key in content:
            out = [
                key,
                get_analysis(key),
                get_method(key),
                '%0.3f' % get_threshold(key),
            ]
            out.extend([
                '%f' % _ for _ in content[key]
            ])
            handle.write("\t".join(out))
            handle.write("\n")

    
