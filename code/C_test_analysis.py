"""
Script carries out the analysis of the test data.

To run this script, make sure you have LingPy (http://lingpy.org) and IGraph
(http://igraph.org) installed. 

"""

from lingpyd import *
from lingpyd.evaluate.acd import *

from P_infomap import infomap_clustering

wordlists = [
        "D_test_Bahnaric-200-24.tsv",
        "D_test_Chinese-180-18.tsv",
        "D_test_Huon-140-14.tsv",
        "D_test_Romance-110-43.tsv",
        "D_test_Tujia-109-5.tsv",
        "D_test_Uralic-173-8.tsv"
        ]

# second block, get the analyses
res = []
for f in wordlists:
    
    # load the wordlist
    try:
        lex = LexStat(f[:-4]+'.bin.tsv')
    except:
        lex = LexStat(f)
        lex.get_scorer(
                preprocessing=False, 
                runs=10000,
                ratio = (2,1),
                vscale = 1.0,

                )
        lex.output('tsv', filename=f[:-4]+'.bin')

    
    # analyze the data
    lex.cluster(method='turchin', ref="turchin")
    lex.cluster(cluster_method='upgma', method='sca', threshold=0.45, ref='sca')
    lex.cluster(cluster_method='upgma', method='edit-dist', threshold=0.75, ref='edit')
    #lex.get_scorer(preprocessing=False, runs=10000)
    lex.cluster(method='lexstat', threshold=0.60, cluster_method='upgma',
            ref="lexstat")
    
    lex.cluster(method='lexstat', threshold=0.55,
            ref='infomap', external_function=infomap_clustering
            )

    # carry out the comparison of the data    
    for eva in ['turchin', 'sca', 'edit', 'lexstat', 'infomap']:
        a,b,c = bcubes(lex, 'cogid', eva, pprint=False)
        print(f[6:-4], '{0:10}'.format(eva), '\t', '\t'.join(['{0:.2f}'.format(x) for x in [a,b,c]]))
        res += [[f,eva, a,b,c]]

    # write data to output file
    lex.output("tsv", filename='O_'+f[2:].split('.')[0], ignore=['json',
            'msa', 'scorer', 'taxa'])

for line in res:
    print(line[0], line[1], '\t'.join(['{0:.2f}'.format(x) for x in line[2:]]))

import json
with open('R_test_results.json','w') as f:
    f.write(json.dumps(res, indent=2))

# print the results for convenience
for eva in ['turchin', 'sca', 'edit', 'lexstat', 'infomap']:
    print(eva, '{0:.4f}'.format(sum([line[-1] for line in res if line[1] == eva]) / 6))
