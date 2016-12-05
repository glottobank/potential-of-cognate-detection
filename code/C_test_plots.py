import json
from matplotlib import pyplot as plt

res = json.loads(open('R_test_results.json').read())

# define a converter for the plots (so that it looks nice afterwards)
converter = {
        'D_test_Bahnaric-200-24.tsv' : 'Bahnaric',
        'D_test_Chinese-180-18.tsv' : 'Chinese',
        'D_test_Romance-110-43.tsv' : 'Romance',
        'D_test_Uralic-173-8.tsv' : 'Uralic',
        'D_test_Tujia-109-5.tsv' : 'Tujia',
        'D_test_Huon-140-14.tsv':'Huon',
        'sca' : 'SCA',
        'turchin' : 'Turchin',
        'edit' : 'Edit Distance',
        'lexstat' : 'LexStat',
        'infomap' : 'LS-Infomap'
        }

# define methods and colors
methods = ['turchin', 'edit', 'sca', 'lexstat', 'infomap']
colors = ['black','white','lightgray','gray','0.2']
colors = ['black', '#a6bddb', '#74c476', '#de2d26', '#ffffbf']
# start creating the figure
plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)


# get full results 
res_precision = []
res_recall = []
res_fscore = []
plt.ylim(0.6,1.0)

# iterate over the results 
for i,method in enumerate(methods): 
    res_precision += [sum([line[2] for line in res if line[1] == method ]) / 6]
    res_recall += [sum([line[3] for line in res if line[1] == method    ]) / 6]
    res_fscore += [sum([line[4] for line in res if line[1] == method    ]) / 6]

    ax.bar(
            [i+1,i+7,i+13],
            [res_precision[-1], res_recall[-1], res_fscore[-1]],
            color=colors[i],
            label = converter[method]
            )
plt.xticks([3,10,17], ['Precision', 'Recall', 'F-Score'])
plt.legend(loc=(0.7,0.1))
plt.savefig('I_results.svg')
plt.savefig('I_results.pdf')
plt.clf()

# write stuff to latex table
with open('T_results_full.tex', 'w') as f:
    txt = ''
    txt = r'\tabular{|l||l|l|l|}\hline'+'\n'
    txt += r'\bf Method & \bf Precision & \bf Recall & \bf F-Score \\\hline\hline'+'\n'
    for i,method in enumerate(methods):
        txt += converter[method] + ' & '
        txt += ' & '.join(['{0:.4f}'.format(s) for s in [
            res_precision[i],
            res_recall[i], 
            res_fscore[i]]]
            )
        txt += r'\\\hline'+'\n'
    txt += r'\endtabular'
    f.write(txt)

# make a figure for the specific results
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(0.6,1)
idx = 0
R = {}
dsets = []
for i,r in enumerate(res):
    
    result = r[-1]
    dset = converter[r[0]]
    method = converter[r[1]]
    try:
        R[dset][method] = result
    except KeyError:
        R[dset] = {method : result}

txt = ''
txt += r'\tabular{|l||l|l|l|l|l|l|}\hline'+'\n'
txt += '&'.join([r'\bf {0}'.format(x) for x in ['Method'] + sorted(R)])
txt += r'\\\hline\hline'+'\n'

txt2 = r'\tabular{|l||l|l|l|l|}\hline'+'\n'
txt2 += r'\bf Dataset & '+'&'.join([converter[m] for m in methods])+r'\\\hline\hline'+'\n'
for i,dset in enumerate(sorted(R)):
    txt2 += dset
    for j,method in enumerate(methods):

        txt2 += '& {0:.4f}'.format(R[dset][converter[method]])
    txt2 += r'\\\hline'+'\n'
txt2 += r'\endtabular'

for i,method in enumerate(methods):
    idxs = []
    ress = []
    for j,dset in enumerate(sorted(R)):

        ress += [R[dset][converter[method]]]


    ax.bar(
            [i+1,i+7,i+13,i+19,i+25,i+31],
            ress, 
            label = converter[method],
            color = colors[i],
            width=0.8
            )
    
    txt += converter[method] + '&' + '&'.join(['{0:.4f}'.format(x) for x in ress])
    txt += r'\\\hline'+'\n'

txt += r'\endtabular'+'\n'
plt.xticks([3,9,15,21,27,33], sorted(R), rotation=45)
plt.legend(loc=(0.525,0.1))
plt.savefig('I_detailed_results.svg')
plt.savefig('I_detailed_results.pdf')
with open('T_detailed_results.tex', 'w') as f:
    f.write(txt2)


