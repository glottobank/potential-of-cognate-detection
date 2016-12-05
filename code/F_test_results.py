#!/usr/bin/env python
#coding=utf-8
import os
import json

FILENAME = "R_test_results.json"

mapper = {
        'infomap' : 'Infomap',
        'lexstat': 'LexStat',
        'sca' : 'SCA',
        'edit' : 'Edit Distance',
        'turchin' : 'Turchin'
        }

if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        raise IOError('Unable to find: %s' % FILENAME)
     
    with open(FILENAME, 'r') as handle:
        content = json.load(handle)
    
    with open(FILENAME.replace(".json", '.txt'), 'w') as handle:
        for row in content:
            row[1] = mapper[row[1]]
            handle.write("\t".join([str(_) for _ in row]))
            handle.write("\n")
