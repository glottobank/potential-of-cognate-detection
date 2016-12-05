from lingpy import *
from lingpy.sequence.sound_classes import token2class, syllabify
from matplotlib import gridspec
from collections import defaultdict
from matplotlib import pyplot as plt

wordlists = [
        "D_test_Bahnaric-200-24.tsv",
        "D_test_Chinese-180-18.tsv",
        "D_test_Huon-140-14.tsv",
        "D_test_Romance-110-43.tsv",
        "D_test_Tujia-109-5.tsv",
        "D_test_Uralic-173-8.tsv",
        ]

data = []
fig = plt.figure()
color = Model('color')
gs = gridspec.GridSpec(len(wordlists)+2, 1)
all_cols = []
all_sounds = defaultdict(int)
all_colors = {}
for i, w in enumerate(wordlists):
    wl = Wordlist(w)
    colors = {}
    tmp = defaultdict(int)
    sylen = []
    clen = []
    for k in wl:
        dolgos = tokens2class(wl[k, 'tokens'], 'dolgo')
        for idx, t in zip(dolgos, wl[k, 'tokens']):
            if idx not in '+':
                tmp[idx] += 1
                colors[idx] = token2class(t, color)
                all_cols += [(k, colors[idx])]
                all_sounds[idx] += 1
                all_colors[idx] = colors[idx]
        sylen += [len(syllabify(' '.join(wl[k, 'tokens']), output='nested'))]
        clen += [len([x for x in dolgos if x not in '1V'])]
    print(w, sum(sylen) / len(sylen), sum(clen) / len(clen))
    ax = plt.subplot(gs[i])
    labels = [x for x, y in sorted(tmp.items(), key=lambda x: x[0])]
    ax.pie([y for x, y in sorted(tmp.items(), key=lambda x: x[0])],
            colors=[y for x, y in sorted(colors.items(), key=lambda x: x[0])],
            radius = 0.95, frame=True, shadow=True)
    ax.set_autoscale_on(False)
    plt.ylim(-1, 1)
    plt.xlim(-1, 1)
    plt.title(w.split('_')[2].split('-')[0])
    plt.axis('off')
    ax.set_aspect('equal')

print('plotting')
ax = plt.subplot(gs[i+1])
ax.pie([y for x, y in sorted(all_sounds.items(), key=lambda x: x[0])],
        colors=[y for x, y in sorted(all_colors.items(), key=lambda x: x[0])],
        radius = 0.95, frame=True, shadow=True)
plt.ylim(-1, 1)
plt.xlim(-1, 1)
plt.title('TOTAL')
plt.axis('off')
ax.set_aspect('equal')
print('legend')
ax = plt.subplot(gs[i+2])
for a, b in sorted(set(all_cols), key=lambda x: x[0]):
    plt.plot(100, 100, 's', label=a, color=b)
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.axis('off')
ax.legend(loc=(0.1, 0.1), prop={'size':6}, numpoints=1)
plt.savefig('distribution-pie.pdf')
print('saved fig')

