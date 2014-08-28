#! /usr/bin/env python

"""
Shipyard-style MiSeq pipeline, post-processing step
Takes CSV file generated by sam2aln.py (corresponding to a sample)
and clips out sequence regions corresponding to sub-regions as
indicated by a CSV file containing the respective nucleotide
reference sequences.

Dependencies:
    hyphyAlign.py
"""

import argparse
import csv
import HyPhy
import itertools
import os

import hyphyAlign
import settings

parser = argparse.ArgumentParser(
    description='Clip out sub-regions from MiSeq read alignments.')

parser.add_argument('aligned_csv', help='<input> CSV containing aligned and merged reads.')
parser.add_argument('nuc_variants', help='<output> CSV containing clipped sequences')

args = parser.parse_args()


hyphy = HyPhy._THyPhy(os.getcwd(), 1)  # @UndefinedVariable
hyphyAlign.change_settings(hyphy, alphabet=hyphyAlign.nucAlphabet,
                           scoreMatrix=hyphyAlign.nucScoreMatrix,
                           gapOpen=20, gapOpen2=20,
                           gapExtend=10, gapExtend2=10,
                           noTerminalPenalty=1)

# distribution of mean alignment scores are very bimodal, easy to split
# note score is incremented by 5 for every matching bp
min_avg_score = 2.


def main():
    # load reference sequences
    is_ref_found = False
    possible_refs = (os.path.basename(settings.final_nuc_align_ref_path),
                     settings.final_nuc_align_ref_path)
    for ref in possible_refs:
        if not os.path.isfile(ref):
            continue
        is_ref_found = True
        break
    if not is_ref_found:
        raise RuntimeError('No reference sequences found in {!r}'.format(
            possible_refs))

    refseqs = {}
    with open(ref, 'rb') as f:
        rows = csv.reader(f)
        for region, _variant, subregion, sequence in rows:
            if region not in refseqs:
                refseqs.update({region: {}})
            refseqs[region][subregion] = sequence

    handle = open(args.aligned_csv, 'rb')
    outfile = open(args.nuc_variants, 'w')
    
    handle.readline() # skip header
    outfile.write('sample,refname,qcut,subregion,index,count,seq\n')

    for key, group in itertools.groupby(handle, lambda x: x.split(',')[0:2]):
        sample_name, refname = key
        if refname not in refseqs:
            continue

        for qcut, group2 in itertools.groupby(group, lambda x: x.split(',')[2]):
            fasta = dict([(subregion, {}) for subregion in refseqs[refname].iterkeys()])
            for line in group2:
                (_sample_name,
                 _refname,
                 _qcut,
                 index,
                 count,
                 _offset,
                 seq) = line.strip('\n').split(',')
                for subregion, refseq in refseqs[refname].iteritems():
                    aquery, aref, ascore = hyphyAlign.pair_align(hyphy, refseq, seq)
                    if float(ascore) / len(refseq) < min_avg_score:
                        continue

                    left, right = hyphyAlign.get_boundaries(aref)
                    clipped_seq = aquery[left:right]
                    if clipped_seq not in fasta[subregion]:
                        fasta[subregion].update({clipped_seq: 0})
                    fasta[subregion][clipped_seq] += int(count)

            # re-compress sequence variants clipped to subregion
            for subregion in fasta.iterkeys():
                intermed = [(count, seq) for seq, count in fasta[subregion].iteritems()]
                intermed.sort(reverse=True)  # descending order
                for index, (count, seq) in enumerate(intermed):
                    outfile.write('%s,%s,%s,%s,%d,%d,%s\n' % (sample_name,
                                                              refname,
                                                              qcut,
                                                              subregion,
                                                              index,
                                                              count,
                                                              seq))

    handle.close()
    outfile.close()


if __name__ == '__main__':
    main()
