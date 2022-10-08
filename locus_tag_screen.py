#! /usr/bin/env python3

import sys
import csv
import json
import argparse
import os
from collections import defaultdict
from tqdm import tqdm
import pathogenprofiler as pp
import tbprofiler as tbprofiler

def main(args):
    if args.samples:
        samples = [x.rstrip() for x in open(args.samples).readlines()]
    else:
        samples = [x.replace(args.suffix,"") for x in os.listdir(args.dir) if x[-len(args.suffix):]==args.suffix]

    OUT = open(args.out,"w")
    writer = csv.DictWriter(OUT, fieldnames = ["sample","genome_pos", "ref", "alt", "type", "nucleotide_change", "protein_change"])
    writer.writeheader()

    for s in tqdm(samples):
        data = json.load(open(pp.filecheck("%s/%s%s" % (args.dir,s,args.suffix))))
        present = False
        resistant_drugs = set()
        for var in data["other_variants"]:
            if var["locus_tag"]=="Rv0005":
                present = True
        if present:
            writer.writerow({"sample":s, "genome_pos":var["genome_pos"], "ref":var["ref"], "alt":var["alt"], "type":var["type"], "nucleotide_change":var["nucleotide_change"], "protein_change":var["protein_change"]})

    OUT.close()

parser = argparse.ArgumentParser(description='tbprofiler script',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--out', type=str, help='Name of CSV output', required=True)
parser.add_argument('--samples', type=str, help='File with samples')
parser.add_argument('--dir', default="results/", type=str, help='Directory containing results')
parser.add_argument('--db', default="tbdb", type=str, help='Database name')
parser.add_argument('--suffix', default=".results.json", type=str, help='File suffix')
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)