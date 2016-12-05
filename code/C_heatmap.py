from lingpy import *
from lingpy.convert.tree import *
from lingpy.convert.plot import plot_heatmap
from P_infomap import *


f = 'D_test_Chinese-180-18.tsv'

try:
    lex = LexStat(f.replace('.tsv','.cog.tsv'))
except: 
    lex = LexStat(f)
    lex.get_scorer()
    lex.calculate('tree', ref='cogid')
    lex.cluster(method='lexstat', threshold=0.6)
    lex.cluster(method='turchin')
    lex.cluster(method='edit-dist', threshold=0.75)
    lex.cluster(method='lexstat', external_function=infomap_clustering,
            threshold=0.55, ref='infomap')
    lex.output('tsv', filename=f.replace('.tsv','.cog'))

tree = """((((((((((Beijing,Shenyang),Jinan),Xian),(Chengdu,Kunming)),(Hefei,Yangzhou)),Changsha),Nanchang),(Suzhou,Wenzhou)),((Guangzhou,Yangjiang),Meixian)),((Chaozhou,Xiamen),Fuzhou));"""

_, tree_taxa = nwk2tree_matrix(tree)

def make_matrix(test):
    matrix = [[0 for i in tree_taxa] for j in tree_taxa]
    for i,tA in enumerate(tree_taxa):
        for j,tB in enumerate(tree_taxa):
            if i < j:
                # get amount of false positives
                count = 0
                fp = 0
                fn = 0
                pairs = (tA, tB) if (tA, tB) in lex.pairs else (tB, tA)
                print(pairs)
                for idxA, idxB in lex.pairs[pairs]:
                    count += 1
                    gids = lex[idxA,'cogid'], lex[idxB,'cogid']
                    tids = lex[idxA, test], lex[idxB, test]
                    # false positive means tids is equal, gids is false
                    if tids[0] == tids[1] and gids[0] != gids[1]:
                        fp += 1
                    # false negative means, gids is equal, tids is unequal
                    if tids[0] != tids[1] and gids[0] == gids[1]:
                        fn += 1
                matrix[i][j] = fp / count
                matrix[j][i] = fn / count
    print(matrix)
    return matrix

matrix = make_matrix('turchinid')
plot_heatmap(lex, filename='heatmap-turchin', vmax=0.3,
        matrix=matrix, tree=tree, colorbar_label='False Positives/Negatives')
matrix = make_matrix('lexstatid')
plot_heatmap(lex, filename='heatmap-lexstat', vmax=0.3, matrix=matrix,
        tree=tree, colorbar_label='False Positives/Negatives')
matrix = make_matrix('editid')
plot_heatmap(lex, filename='heatmap-edit', vmax=0.3, matrix=matrix, tree=tree, colorbar_label='False Positives/Negatives')

matrix = make_matrix('infomap')
plot_heatmap(lex, filename='heatmap-infomap', vmax=0.3, matrix=matrix, tree=tree, colorbar_label='False Positives/Negatives')
