import json

with open('R_training_results.json') as f:
    R = json.loads(f.read())

wordlists = [
        "D_training_Austronesian-210-20.tsv",
        "D_training_Bai-110-09.tsv",
        "D_training_Chinese-140-15.tsv",
        "D_training_IndoEuropean-207-20.tsv",
        "D_training_Japanese-200-10.tsv",
        "D_training_ObUgrian-110-21.tsv",
        ]

score = sum([R['1/turchin/'+w][-1] for w in wordlists]) / len(wordlists)
print('turchin', 0,'{0:.2f}'.format(score))

scores = [[],[],[],[],[]]
best_idxs = [0,0,0,0,0]
best_scores = [0,0,0,0,0]
for i in range(2,19):
    score = sum([R[str(i)+'/lexstat/'+w][-1] for w in wordlists]) / len(wordlists)
    scores[2] += [score]
    print('lexstat', i,'{0:.4f}'.format(score))
    if best_scores[2] < score:
        best_idxs[2] = i
        best_scores[2] = score

for i in range(2,19):
    score = sum([R[str(i)+'/infomap/'+w][-1] for w in wordlists]) / len(wordlists)
    print('infomap', i,'{0:.4f}'.format(score))
    scores[4] += [score]
    if best_scores[4] < score:
        best_idxs[4] = i
        best_scores[4] = score

for i in range(2,19):
    score = sum([R[str(i)+'/sca/'+w][-1] for w in wordlists]) / len(wordlists)
    print('sca', i,'{0:.4f}'.format(score))
    scores[1] += [score]
    if best_scores[1] < score:
        best_idxs[1] = i
        best_scores[1] = score
for i in range(2,19):
    score = sum([R[str(i)+'/edit/'+w][-1] for w in wordlists]) / len(wordlists)
    print('edit', i,'{0:.4f}'.format(score))
    scores[0] += [score]
    if best_scores[0] < score:
        best_idxs[0] = i
        best_scores[0] = score

for i in range(2,19):
    score = sum([R[str(i)+'/mcl/'+w][-1] for w in wordlists]) / len(wordlists)
    print('mcl', i,'{0:.4f}'.format(score))
    scores[3] += [score]
    if best_scores[3] < score:
        best_idxs[3] = i
        best_scores[3] = score

ts = [0.05 * i for i in range(2,19)]

# make a boxplot with matplotlib
from matplotlib import pyplot as plt
plt.clf()
colors = ['black', 'gray', 'lightgray', 'white', '0.8']
markers = ['o','o','o','o','s']
labels=['Edit Distance', 'SCA', 'LexStat',
    'MCL', 'Infomap']
for i,score in enumerate(scores):
    plt.plot(ts[0], score[0],markers[i], label=labels[i], color=colors[i])
    for j,s in enumerate(score):
        plt.plot(ts[j], s, markers[i], color=colors[i])

# write latex-table or similar
best_idxs = [1] + best_idxs
nlabels = ['Turchin'] + [x for x in labels]
for i,(idx,method) in enumerate(zip(best_idxs, ['turchin', 'edit', 'sca', 'lexstat',
    'mcl', 'infomap'])):

    p = sum([R[str(idx)+'/'+method+'/'+w][0] for w in wordlists]) / len(wordlists)
    r = sum([R[str(idx)+'/'+method+'/'+w][1] for w in wordlists]) / len(wordlists)
    f = sum([R[str(idx)+'/'+method+'/'+w][2] for w in wordlists]) / len(wordlists)
    print(nlabels[i]+'& {0:.2f} & '.format(idx * 0.05)+'{0:.4f} & {1:.4f} & {2:.4f}'.format(p, r,
        f)+r'\\\hline')


plt.xlim(0.01,0.95)
plt.legend(loc=(0.5,0.1), numpoints=1)

plt.savefig('I_training_results.pdf')

plt.clf()
# make errorbar analysis
names = ['edit', 'sca', 'lexstat', 'infomap']
scores = [str(best_idxs[i]) for i in [1,2,3,5]] # ['15', '9', '12', '11']
colors = ['#a6bddb', '#74c476', '#de2d26', '#ffffbf']
dsets = ['Austronesian', 'Bai', 'Chinese', 'IndoEuropean', 'Japanese',
        'ObUgrian']
symbols = ['.', ',', 'o', 'v', '^', 's']
dsetcols = ['red','blue','green', 'black', 'white', 'gray']

for i,name in enumerate(names): # in zip(names, scores, colors):
    f = plt.figure()
    dlables = ['{0:.2f}'.format(x * 0.05) for x in range(2,19)]
    drange = list(range(2,19))
    alldata = []
    means = []
    for j in range(2,19):
        data = [R[z][-1] for z in R if str(j)+'/'+name in z]
        alldata += [data]
    bp = plt.boxplot(alldata, patch_artist=True
           )
    for j,dpoint in enumerate(alldata):
        if str(j+2) == scores[i]:
            color = 'black'
            marker = 'v'
            size = 10
        else:
            color = 'black'
            marker = 'o'
            size = 5
        plt.plot(j+1, sum(dpoint)/len(dpoint), marker, color=color,
                markersize=size)

    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['boxes'], facecolor=colors[i])
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['medians'], color='black')
    plt.setp(bp['caps'], color=colors[i])
    plt.setp(bp['fliers'], marker='None')
    plt.xlim(0,18)
    plt.xticks(range(1,18,2), ['{0:.2f}'.format(x * 0.1) for x in range(1,10)])
    plt.ylim(0,1)
    plt.savefig(name+'.pdf')
    plt.clf()
        
