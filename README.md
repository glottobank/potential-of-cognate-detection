# The Potential of Automatic Word Comparison for Historical Linguistics: Source Code and Data

This repository provides source code and data for the paper on the potential of automatic word comparison for historical linguistics (List, Greenhill, and Gray).

## Requirements

You will need LingPy (v >= 2.5, http://github.com/lingpy.lingpy), python-igraph (http://igraph.org/python-igraph), and the requirements which are needed for both packages. You will also need R if you want to make all plots that we prepared for the analyses.

## Code

To simply run all analyses, open your terminal, make sure you cd ino the folder and type:

```shell
$ make all
```

This will run both the training and the test analyses. Note, however, that this analyses uses the results of the Monte-Carlo permutation, which is very time-consuming, and whose results we submit along with the data-files which have a "bin.tsv" extension. If you want to re-run the Monte-Carlo permutation, you should first remove these files from the directory. You can also do this by typing:

```shell
$ make clean
```

If you run the analyses along with the Monte-Carlo permutation, this will take some time. All code pieces which you need to run the analyses are prefixed by `C_` in the file-collection.

## Datasets

All datasets in this sample are prefixed by `D_`. There are 12 datasets, 6 training datasets, prefixed by `D_training`, and 6 test datasets, prefixed by `D_test`. For the sources of the data, please consult the paper, which is submitted along with this repository.

## Infomap-Plugin

The Infomap plugin (see the pape for details) is in the file `P_infomap.py`. As of lingpy-2.5, this plugin is also regularly integrated into the library. However, this repository provides the original version that uses it as a plugin to lingpy.

## Output Created by the Scripts

There are four kinds of output created by the scripts:

* simple tsv-files, all prefixed with `O_`+`test` or `training`, depending on which file was analyzed,
* plots, all prefixed with `I_`
* LaTeX tables, all prefixed with `T_`
* txt-result files, all prefixed with `R_`

## Questions

If you run into problems or have further questions regarding the data, please contact us writing an email to info@lingpy.org.
