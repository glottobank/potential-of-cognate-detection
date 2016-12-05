"""
Test the training data in order to determine the best threshold for each method.
"""

from lingpy import *
from lingpy.evaluate.acd import *
from P_infomap import infomap_clustering

# define wordlists which are used for training
wordlists = [
        "D_training_Bai-110-09.tsv",
        "D_training_Austronesian-210-20.tsv",
        "D_training_Chinese-140-15.tsv",
        "D_training_IndoEuropean-207-20.tsv",
        "D_training_Japanese-200-10.tsv",
        "D_training_ObUgrian-110-21.tsv",
        ]

# get statistics regarding the test data, this is just to make sure the data
# contains the same points we mentioned in the paper
wlen = 0
wh = 0
ww = 0
wc = 0
dv = 0
for f in wordlists:
    wl = Wordlist(f)
    etd = wl.get_etymdict(ref='cogid')
    wlen += len(wl)
    wh += wl.height
    ww += wl.width
    wc += len(etd)
    div = (len(etd) - wh) / (len(wl) - wh)
    dv += div
    print(f, '&', len(wl),'&', wl.height,'&', wl.width,'&', len(etd), '&',
            '{0:.2f}'.format(div), r'& \\\hline')
print(f, '&', wlen,'&', wh,'&', ww,'&', wc, '&', '{0:.2f}'.format(dv / 6), r'& \\\hline')
wlen = 0
wh = 0
ww = 0
wc = 0
dv = 0

for f in wordlists:
    wl = Wordlist(f)
    etd = wl.get_etymdict(ref='cogid')
    wlen += len(wl)
    wh += wl.height
    ww += wl.width
    wc += len(etd)
    div = (len(etd) - wl.height) / (len(wl) - wl.height)
    dv += div
    print(f[11:f.index('-')], '\t', len(wl),'\t', wl.height,'\t', wl.width,'\t', len(etd), '\t',
            '{0:.2f}'.format(div))
print('TOTAL', '\t', wlen,'\t', wh,'\t', ww,'\t', wc, '\t', '{0:.2f}'.format(dv / 6) )
# carry out the real analyses
res = []
D = dict([(i,{}) for i in range(1,19)])
for f in wordlists:
    
    try:
        lex = LexStat(f[:-4]+'.bin.tsv')
    except:
        lex = LexStat(f)
        lex.get_scorer(preprocessing=False, runs=10000, ratio=(2,1), vscale=1.0)
        lex.output('tsv', filename=f[:-4]+'.bin')
    
    lex.cluster(method='turchin', ref='turchin')

    for i in range(2,19):

        lex.cluster(cluster_method='upgma', method='sca', threshold=0.05 * i, ref='sca-'+str(i))
        lex.cluster(cluster_method='upgma', method='lexstat', threshold=0.05 * i, ref="lexstat-"+str(i))
        lex.cluster(cluster_method='upgma', method='edit-dist', threshold=0.05 * i, ref="edit-"+str(i))

        lex.cluster(method='lexstat', threshold=0.05 *
                i, ref='infomap-'+str(i),
                external_function=infomap_clustering
                )
        lex.cluster(method='lexstat', threshold=0.05 *
                i, ref='mcl-'+str(i),
                cluster_method='mcl'
                )

    # get the evaluation scores
    a,b,c = bcubes(lex, 'cogid', 'turchin', pprint=False)
    
    # write the turchin score to file
    print(f, 'turchin', '\t', '\t'.join(['{0:.2f}'.format(x) for x in [a,b,c]]))
    res += [[f, 'turchin', a,b,c]]
    D[1]['turchin',f] = [a,b,c]
    
    # get results for infomap
    best = 0
    scores = []
    for i in range(2,19):
        a,b,c = bcubes(lex, 'cogid', 'infomap-'+str(i), pprint=False)
        if c > best:
            best = c
            scores = [a,b,c,'cogid','infomap-'+str(i)]
        D[i]['infomap',f] = [a,b,c]
    res += [[f, scores[-1], scores[0], scores[1], scores[2]]]
    print(f, '', '\t', '\t'.join(['{0:.2f}'.format(x) for x in scores[:3]]),
        '\t',scores[-1])
    
    # get results for SCA 
    best = 0
    scores = []
    for i in range(2,19):
        a,b,c = bcubes(lex, 'cogid', 'sca-'+str(i), pprint=False)
        if c > best:
            best = c
            scores = [a,b,c,'cogid','sca-'+str(i)]
        D[i]['sca',f] = [a,b,c]
    res += [[f, scores[-1], scores[0], scores[1], scores[2]]]

    # get results for edit-distance
    best,scores = 0,[]
    for i in range(2,19):
        a,b,c = bcubes(lex, 'cogid', 'edit-'+str(i), pprint=False)
        if c > best:
            best = c
            scores = [a,b,c,'cogid','edit-'+str(i)]
        D[i]['edit',f] = [a,b,c]
    res += [[f, scores[-1], scores[0], scores[1], scores[2]]]

    print(f, '', '\t', '\t'.join(['{0:.2f}'.format(x) for x in scores[:3]]),
        '\t',scores[-1])

    # get results for lexstat
    scores = []
    best = 0
    for i in range(2,19):
        a,b,c = bcubes(lex, 'cogid', 'lexstat-'+str(i), pprint=False)
        if c > best:
            best = c
            scores = [a,b,c,'lexstat-'+str(i)]
        D[i]['lexstat',f] = [a,b,c]
    res += [[f, scores[-1], scores[0], scores[1], scores[2]]]
    print(f, '', '\t', '\t'.join(['{0:.2f}'.format(x) for x in scores[:3]]))

    # get results for mcl 
    scores = []
    best = 0
    for i in range(2,19):
        a,b,c = bcubes(lex, 'cogid', 'mcl-'+str(i), pprint=False)
        if c > best:
            best = c
            scores = [a,b,c,'lexstat-'+str(i)]
        D[i]['mcl',f] = [a,b,c]
    res += [[f, scores[-1], scores[0], scores[1], scores[2]]]
    print(f, '', '\t', '\t'.join(['{0:.2f}'.format(x) for x in scores[:3]]))

    # write data to file
    lex.output('tsv',
            filename='O_'+f[2:].replace('.tsv',''),
            ignore = ['msa', 'taxa', 'scorer', 'json'])

import json
R = {}
for k in D:
   for a,b in D[k]:
       R[str(k)+'/'+a+'/'+b] = D[k][a,b]
with open('R_training_results.json', 'w') as f:
    f.write(json.dumps(R, indent=2))

