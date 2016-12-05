from lingpy import *
from P_infomap import infomap_clustering

wordlists = [
        "D_test_Bahnaric-200-24.tsv",
        "D_test_Chinese-180-18.tsv",
        "D_test_Huon-140-14.tsv",
        "D_test_Romance-110-43.tsv",
        "D_test_Tujia-109-5.tsv",
        "D_test_Uralic-173-8.tsv",
        #"D_training_Bai-110-09.tsv",
        "D_training_Austronesian-210-20.tsv",
        #"D_training_Chinese-140-15.tsv",
        "D_training_IndoEuropean-207-20.tsv",
        #"D_training_Japanese-200-10.tsv",
        #"D_training_ObUgrian-110-21.tsv",
        ]
for f in wordlists:
    
    try:
        wl = Wordlist(f.replace('tsv', 'cog.tsv'))
    except:
        lex = LexStat(f)
        lex.cluster(method='turchin')
        lex.get_scorer(preprocessing=False, runs=10000)
        lex.cluster(method='lexstat', ref='infomap', threshold=0.55,
                external_function=infomap_clustering)
        lex.output('tsv', filename=f.replace('.tsv', '.cog'), ignore='all',
                prettify=False)
        wl = Wordlist(lex)
    for m in ['cogid', 'turchinid', 'infomap']:

        wl.output('paps.nex', ref=m, filename='N_'+f.split('_')[2]+'-'+m)

