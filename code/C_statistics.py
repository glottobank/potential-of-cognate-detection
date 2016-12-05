from lingpy import *
wordlists1 = [
        "D_test_Bahnaric-200-24.tsv",
        "D_test_Chinese-180-18.tsv",
        "D_test_Huon-140-14.tsv",
        "D_test_Romance-110-43.tsv",
        "D_test_Tujia-109-5.tsv",
        "D_test_Uralic-173-8.tsv"
        ]
wordlists2 = [
        "D_training_Bai-110-09.tsv",
        "D_training_Austronesian-210-20.tsv",
        "D_training_Chinese-140-15.tsv",
        "D_training_IndoEuropean-207-20.tsv",
        "D_training_Japanese-200-10.tsv",
        "D_training_ObUgrian-110-21.tsv",
        ]

def print_summary(wordlists):
    sums = [0,0,0,0,0]
    for f in wordlists:
        name = f.split('_')[-1]
        wl = Wordlist(f)
        etd = wl.get_etymdict(ref='cogid')
    
        words = len(wl)
        cogs = len(etd)
        concepts = wl.height
        taxa = wl.width
    
        wl.calculate('diversity')
        diversity = wl.diversity

        sums[0] += words
        sums[3] += cogs
        sums[1] += concepts
        sums[2] += taxa
        sums[4] += diversity
    
        print(' & '.join([
            name[:name.index('-')],
            str(words),
            str(concepts),
            str(taxa),
            str(cogs),
            '{0:.2f}'.format(diversity)])+r'\\\hline')
    print('TOTAL & {0[0]} & {0[1]} & {0[2]} & {0[3]} & {1:.2f}'.format(sums,
        sums[-1] / len(wordlists)))

print_summary(wordlists1)
print('')
print_summary(wordlists2)
