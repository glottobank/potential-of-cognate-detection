from lingpy import *
from P_infomap import *
from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
wordlists = [
        "D_test_Bahnaric-200-24.tsv",
        "D_test_Chinese-180-18.tsv",
        "D_test_Huon-140-14.tsv",
        "D_test_Romance-110-43.tsv",
        "D_test_Tujia-109-5.tsv",
        "D_test_Uralic-173-8.tsv"
        ]

gs = gridspec.GridSpec(len(wordlists)+2, 6)

fig = plt.figure()

counter = 0
tcounts = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
ttotals = [0 for x in range(len(wordlists))]
colors = ['lightskyblue', 'crimson', 'lightsalmon', 'blue']
results_file = open('R_false_positives.tsv', 'w')
for path in wordlists:
    print(path)

    try:
        lex = LexStat(path.replace('.tsv', '.cog.tsv'))
    except:
        lex = LexStat(path)
        lex.get_scorer(runs=10000)
        lex.cluster(method='turchin')
        lex.cluster(method='edit-dist', threshold=0.75)
        lex.cluster(method='sca', threshold=0.45)
        lex.cluster(method='lexstat', threshold=0.6)
        lex.cluster(method='lexstat', external_function=infomap_clustering,
                threshold=0.55, ref='infomap')
        lex.output('tsv', filename=path.replace('.tsv', '.cog'),
                prettify=False, ignore='all')

    # get false positives and false negatives
    counts = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0,
        0]] 
    totals = 0
    for i, tA in enumerate(lex.cols):
        for j, tB in enumerate(lex.cols):
            if i < j:
                tpairs = (tA, tB) if (tA, tB) in lex.pairs else (tB, tA)
                for idxA, idxB in lex.pairs[tpairs]:
                    totals += 1 
                    for k, method in enumerate(
                            ['turchinid', 
                                'editid', 
                                'scaid', 
                                'lexstatid',
                                'infomap']
                            ):
                        if method not in lex.header:
                            raise ValueError('no analysis was carried out')
                        gids = lex[idxA, 'cogid'], lex[idxB, 'cogid']
                        tids = lex[idxA, method], lex[idxB, method]
                        
                        # true positives and false negatives
                        if gids[0] == gids[1]:
                            if tids[0] == tids[1]:
                                counts[k][0] += 1
                            else:
                                counts[k][1] += 1
                        else:
                            # false positive
                            if tids[0] == tids[1]:
                                counts[k][3] += 1
                            else:
                                # true negative
                                counts[k][2] += 1

    methods = ['Turchin', 'Edit-Dist.', 'SCA', 'LexStat', 'Infomap']
    for i in range(5):
        ax = plt.subplot(gs[counter * 6 + i])
        ax.pie([x for x in counts[i]], 
            colors = colors, #['red', 'green', 'black', 'yellow'], 
            radius=0.95, frame=True, 
            shadow=True, 
            explode=(0.05, 0.2, 0.05, 0.2),
        )
        ax.set_autoscale_on(False)
        if path == wordlists[0]: plt.title(methods[i])
        plt.ylim(-1, 1)
        plt.xlim(-1, 1)
        plt.axis('off')
        
        ax.set_aspect('equal')
        for k in range(4):
            tcounts[i][k] += counts[i][k] 

        results_file.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(
            path.split('/')[-1].split('_')[2].split('-')[0],
            method,
            counts[i][0], counts[i][1], counts[i][2], counts[i][3]))

        

    ax = plt.subplot(gs[counter * 6 + 5])
    ax.text(0, 0, path.split('-')[0][7:])
    plt.ylim(-1, 1)
    plt.xlim(-1, 1)
    plt.axis('off')
    counter += 1


for i in range(5):
    ax = plt.subplot(gs[counter * 6 + i])
    ax.pie([x for x in tcounts[i]], colors=colors, radius=0.95,
            frame=True, explode=(0.05, 0.2, 0.05, 0.2),
            shadow=True)
    ax.set_autoscale_on(False)
    plt.ylim(-1, 1)
    plt.xlim(-1, 1)
    ax.set_aspect('equal')
    plt.axis('off')

    results_file.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(
        'TOTAL',
        methods[i],
        tcounts[i][0], tcounts[i][1], tcounts[i][2], tcounts[i][3]))
results_file.close()

ax = plt.subplot(gs[counter * 6 + 5])
ax.text(0, 0, 'TOTAL')
plt.ylim(-1, 1)
plt.xlim(-1, 1)
plt.axis('off')

counter += 1

ax = plt.subplot(gs[counter * 6 + 5])

for i, lab in enumerate(['true positive', 'false negative', 'true negative', 
        'false positive']):
    ax.plot(100, 100, 'o', label=lab, color=colors[i])
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.axis('off')
    ax.set_aspect('equal')
    plt.axis('equal')

ax.legend(loc=(0.1, 0.1), prop={"size":6}, numpoints=1)
plt.savefig('A_pie_charts.pdf')
plt.clf()

