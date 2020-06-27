#!/usr/bin/env python3

import plotly.graph_objects as go
import lizard

import os
import sys
import statistics
from tqdm import *

def plot(nlocs, files, parents, ccns):

    fig = go.Figure(go.Treemap(
        labels = files,
        values = nlocs,
        parents = parents,
        marker=dict(
            colors=ccns,
            colorscale='blues',
            cmid=statistics.mean(ccns)),
    ))

    fig.show()


def calc_cc(file_name):
    tmp = lizard.analyze_file(file_name)
    nloc = tmp.nloc
    ccs = []

    for i in range(len(tmp.function_list)):
        ccs.append(tmp.function_list[i].cyclomatic_complexity)

    if not ccs:
        return nloc, 0

    return nloc , statistics.sum(ccs)

def main():
    startpath = sys.argv[1]

    nlocs = []
    files = []
    parents = []
    ccns = []
    exts = ["html","c", "cpp", "cc", "cxx" , "java", "cs", "js", "ejs", "rs", "go", "php", "py"]

    for root, dirs, ffiles in os.walk(startpath):
        for d in dirs:
            nlocs.append(0)
            ccns.append(0)
            files.append(os.path.join(root,d))
            parents.append(root)
        for f in tqdm(ffiles, leave=False):
            if f.split(".")[-1] in exts:
                nloc, ccn = calc_cc(os.path.join(root,f))
                nlocs.append(nloc)
                ccns.append(ccn)
                files.append(os.path.join(root,f))
                parents.append(root)

    plot(nlocs, files, parents, ccns)

if __name__ == '__main__':
    main()
