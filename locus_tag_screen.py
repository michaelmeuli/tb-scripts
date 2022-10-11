#! /usr/bin/env python3

from cgitb import small
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

    print(len(samples))
    sample_nr = 0
    sample_positiv_count = 0

    OUT = open(args.out,"w")
    writer = csv.DictWriter(OUT, fieldnames = ["sample", "locus_tag", "genome_pos", "ref", "alt", "type", "nucleotide_change", "protein_change", "sample_nr", "sample_positiv_count", "sample_total_nr"])
    writer.writeheader()

    for s in tqdm(samples):
        sample_nr += 1
        data = json.load(open(pp.filecheck("%s/%s%s" % (args.dir,s,args.suffix))))
        
        new = False
        for var in data["dr_variants"]:
            if var["locus_tag"]==args.lt:
                new = True
        if new:
            sample_positiv_count +=1

        for var in data["dr_variants"]:
            if var["locus_tag"]==args.lt:
                writer.writerow({"sample":s, "locus_tag":var.get("locus_tag", "NA"), "genome_pos":var.get("genome_pos", "NA"), "ref":var.get("ref", "NA"), "alt":var.get("alt", "NA"), "type":var.get("type", "NA"), "nucleotide_change":var.get("nucleotide_change", "NA"), "protein_change":var.get("protein_change", "NA"), "sample_nr":sample_nr, "sample_positiv_count":sample_positiv_count, "sample_total_nr":len(samples)})      

    OUT.close()

parser = argparse.ArgumentParser(description='tbprofiler script',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--out', type=str, help='Name of CSV output', required=True)
parser.add_argument('--samples', type=str, help='File with samples')
parser.add_argument('--dir', default="results/", type=str, help='Directory containing results')
parser.add_argument('--db', default="tbdb", type=str, help='Database name')
parser.add_argument('--suffix', default=".results.json", type=str, help='File suffix')
parser.add_argument('--lt', default="Rv0005", type=str, help='Locus tag to screen')
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)
