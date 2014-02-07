"""
Perform pairwise alignment of sequence against a reference using the
HyPhy shared library function AlignSequences().
"""

import HyPhy
import re


# CfE reference sequences (A hybrid of HXB2 and consensus B)

refSeqs = {	'DRT clinical': 		"CCTCAGGTCACTCTTTGGCAACGACCCCTCGTCACAATAAAGATAGGGGGGCAACTAAAGGAAGCTCTATTAGATACAGGAGCAGATGATACAGTATTAGAAGAAATGAGTTTGCCAGGAAGATGGAAACCAAAAATGATAGGGGGAATTGGAGGTTTTATCAAAGTAAGACAGTATGATCAGATACTCATAGAAATCTGTGGACATAAAGCTATAGGTACAGTATTAGTAGGACCTACACCTGTCAACATAATTGGAAGAAATCTGTTGACTCAGATTGGTTGCACTTTAAATTTTCCCATTAGCCCTATTGAGACTGTACCAGTAAAATTAAAGCCAGGAATGGATGGCCCAAAAGTTAAACAATGGCCATTGACAGAAGAAAAAATAAAAGCATTAGTAGAAATTTGTACAGAGATGGAAAAGGAAGGGAAAATTTCAAAAATTGGGCCTGAAAATCCATACAATACTCCAGTATTTGCCATAAAGAAAAAAGACAGTACTAAATGGAGAAAATTAGTAGATTTCAGAGAACTTAATAAGAGAACTCAAGACTTCTGGGAAGTTCAATTAGGAATACCACATCCCGCAGGGTTAAAAAAGAAAAAATCAGTAACAGTACTGGATGTGGGTGATGCATATTTTTCAGTTCCCTTAGATGAAGACTTCAGGAAGTATACTGCATTTACCATACCTAGTATAAACAATGAGACACCAGGGATTAGATATCAGTACAATGTGCTTCCACAGGGATGGAAAGGATCACCAGCAATATTCCAAAGTAGCATGACAAAAATCTTAGAGCCTTTTAGAAAACAAAATCCAGACATAGTTATCTATCAATACATGGATGATTTGTATGTAGGATCTGACTTAGAAATAGGGCAGCATAGAACAAAAATAGAGGAGCTGAGACAACATCTGTTGAGGTGGGGACTTACCACACCAGACAAAAAACATCAGAAAGAACCTCCATTCCTTTGGATGGGTTATGAACTCCATCCTGATAAATGGACAGTACAGCCTATAGTGCTGCCAGAAAAAGACAGCTGGACTGTCAATGACATACAGAAGTTAGTGGGGAAATTGAATTGGGCAAGTCAGATTTACCCAGGGATTAAAGTAAGGCAATTATGTAAACTCCTTAGAGGAACCAAAGCACTAACAGAAGTAATACCACTAACAGAAGAAGCAGAGCTAGAACTGGCAGAAAACAGAGAGATTCTAAAAGAACCAGTACATGGAGTGTATTATGACCCATCAAAAGACTTAATAGCAGAAATACAGAAGCAGGGGCAAGGCCAATGGACATATCAAATTTATCAAGAGCCATTTAAAAATCTGAAAACAGGAAAATATGCAAGAATGAGGGGTGCCCACACTAATGATGTAAAACAATTAACAGAGGCAGTGCAAAAAATAACCACAGAAAGCATAGTAATATGGGGAAAGACTCCTAAATTTAAACTGCCCATACAAAAGGAAACATGGGAAACA",
            'POL1017 clinical':		"CCTCAGGTCACTCTTTGGCAACGACCCCTCGTCACAATAAAGATAGGGGGGCAACTAAAGGAAGCTCTATTAGATACAGGAGCAGATGATACAGTATTAGAAGAAATGAGTTTGCCAGGAAGATGGAAACCAAAAATGATAGGGGGAATTGGAGGTTTTATCAAAGTAAGACAGTATGATCAGATACTCATAGAAATCTGTGGACATAAAGCTATAGGTACAGTATTAGTAGGACCTACACCTGTCAACATAATTGGAAGAAATCTGTTGACTCAGATTGGTTGCACTTTAAATTTTCCCATTAGCCCTATTGAGACTGTACCAGTAAAATTAAAGCCAGGAATGGATGGCCCAAAAGTTAAACAATGGCCATTGACAGAAGAAAAAATAAAAGCATTAGTAGAAATTTGTACAGAGATGGAAAAGGAAGGGAAAATTTCAAAAATTGGGCCTGAAAATCCATACAATACTCCAGTATTTGCCATAAAGAAAAAAGACAGTACTAAATGGAGAAAATTAGTAGATTTCAGAGAACTTAATAAGAGAACTCAAGACTTCTGGGAAGTTCAATTAGGAATACCACATCCCGCAGGGTTAAAAAAGAAAAAATCAGTAACAGTACTGGATGTGGGTGATGCATATTTTTCAGTTCCCTTAGATGAAGACTTCAGGAAGTATACTGCATTTACCATACCTAGTATAAACAATGAGACACCAGGGATTAGATATCAGTACAATGTGCTTCCACAGGGATGGAAAGGATCACCAGCAATATTCCAAAGTAGCATGACAAAAATCTTAGAGCCTTTTAGAAAACAAAATCCAGACATAGTTATCTATCAATACATGGATGATTTGTATGTAGGATCTGACTTAGAAATAGGGCAGCATAGAACAAAAATAGAGGAGCTGAGACAACATCTGTTGAGGTGGGGACTTACCACACCAGACAAAAAACATCAGAAAGAACCTCCATTCCTTTGGATGGGTTATGAACTCCATCCTGATAAATGGACAGTATCCTTTAACTTCCCTCAGGTCACTCTTTGGCAACGACCCCTCGTCACAATAAAGATAGGGGGGCAACTAAAGGAAGCTCTATTAGATACAGGAGCAGATGATACAGTATTAGAAGAAATGAGTTTGCCAGGAAGATGGAAACCAAAAATGATAGGGGGAATTGGAGGTTTTATCAAAGTAAGACAGTATGATCAGATACTCATAGAAATCTGTGGACATAAAGCTATAGGTACAGTATTAGTAGGACCTACACCTGTCAACATAATTGGAAGAAATCTGTTGACTCAGATTGGTTGCACTTTAAATTTTCCCATTAGCCCTATTGAGACTGTACCAGTAAAATTAAAGCCAGGAATGGATGGCCCAAAAGTTAAACAATGGCCATTGACAGAAGAAAAAATAAAAGCATTAGTAGAAATTTGTACAGAGATGGAAAAGGAAGGGAAAATTTCAAAAATTGGGCCTGAAAATCCATACAATACTCCAGTATTTGCCATAAAGAAAAAAGACAGTACTAAATGGAGAAAATTAGTAGATTTCAGAGAACTTAATAAGAGAACTCAAGACTTCTGGGAAGTTCAATTAGGAATACCACATCCCGCAGGGTTAAAAAAGAAAAAATCAGTAACAGTACTGGATGTGGGTGATGCATATTTTTCAGTTCCCTTAGATGAAGACTTCAGGAAGTATACTGCATTTACCATACCTAGTATAAACAATGAGACACCAGGGATTAGATATCAGTACAATGTGCTTCCACAGGGATGGAAAGGATCACCAGCAATATTCCAAAGTAGCATGACAAAAATCTTAGAGCCTTTTAGAAAACAAAATCCAGACATAGTTATCTATCAATACATGGATGATTTGTATGTAGGATCTGACTTAGAAATAGGGCAGCATAGAACAAAAATAGAGGAGCTGAGACAACATCTGTTGAGGTGGGGACTTACCACACCAGACAAAAAACATCAGAAAGAACCTCCATTCCTTTGGATGGGTTATGAACTCCATCCTGATAAATGGACAGTACAGCCTATAGTG",
            'gp41':					"GCAGTGGGAATAGGAGCTTTGTTCCTTGGGTTCTTGGGAGCAGCAGGAAGCACTATGGGCGCAGCCTCAATGACGCTGACGGTACAGGCCAGACAATTATTGTCTGGTATAGTGCAGCAGCAGAACAATTTGCTGAGGGCTATTGAGGCGCAACAGCATCTGTTGCAACTCACAGTCTGGGGCATCAAGCAGCTCCAGGCAAGAATCCTGGCTGTGGAAAGATACCTAAAGGATCAACAGCTCCTGGGGATTTGGGGTTGCTCTGGAAAACTCATTTGCACCACTGCTGTGCCTTGGAATGCTAGTTGGAGTAATAAATCTCTGGAACAGATTTGGAATCACACGACCTGGATGGAGTGGGACAGAGAAATTAACAATTACACAAGCTTAATACACTCCTTAATTGAAGAATCGCAAAACCAGCAAGAAAAGAATGAACAAGAATTATTGGAATTAGATAAATGGGCAAGTTTGTGGAATTGGTTTAACATAACAAATTGGCTGTGGTATATAAAATTATTCATAATGATAGTAGGAGGCTTGGTAGGTTTAAGAATAGTTTTTGCTGTACTTTCTATAGTGAATAGAGTTAGGCAGGGATATTCACCATTATCGTTTCAGACCCACCTCCCAACCCCGAGGGGACCCGACAGGCCCGAAGGAATAGAAGAAGAAGGTGGAGAGAGAGACAGAGACAGATCCATTCGATTAGTGAACGGATCCTTGGCACTTATCTGGGACGATCTGCGGAGCCTGTGCCTCTTCAGCTACCACCGCTTGAGAGACTTACTCTTGATTGTAACGAGGATTGTGGAACTTCTGGGACGCAGGGGGTGGGAAGCCCTCAAATATTGGTGGAATCTCCTACAGTATTGGAGTCAGGAACTAAAGAATAGTGCTGTTAGCTTGCTCAATGCCACAGCCATAGCAGTAGCTGAGGGGACAGATAGGGTTATAGAAGTAGTACAAGGAGCTTGTCAGAGAGAAAAAAGAGCAGTGGGAATAGGAGCTTTGTTCCTTGGGTTCTTGGGAGCAGCAGGAAGCACTATGGGCGCAGCCTCAATGACGCTGACGGTACAGGCCAGACAATTATTGTCTGGTATAGTGCAGCAGCAGAACAATTTGCTGAGGGCTATTGAGGCGCAACAGCATCTGTTGCAACTCACAGTCTGGGGCATCAAGCAGCTCCAGGCAAGAATCCTGGCTGTGGAAAGATACCTAAAGGATCAACAGCTCCTGGGGATTTGGGGTTGCTCTGGAAAACTCATTTGCACCACTGCTGTGCCTTGGAATGCTAGTTGGAGTAATAAATCTCTGGAACAGATTTGGAATCACACGACCTGGATGGAGTGGGACAGAGAAATTAACAATTACACAAGCTTAATACACTCCTTAATTGAAGAATCGCAAAACCAGCAAGAAAAGAATGAACAAGAATTATTGGAATTAGATAAATGGGCAAGTTTGTGGAATTGGTTTAACATAACAAATTGGCTGTGGTATATAAAATTATTCATAATGATAGTAGGAGGCTTGGTAGGTTTAAGAATAGTTTTTGCTGTACTTTCTATAGTGAATAGAGTTAGGCAGGGATATTCACCATTATCGTTTCAGACCCACCTCCCAACCCCGAGGGGACCCGACAGGCCCGAAGGAATAGAAGAAGAAGGTGGAGAGAGAGACAGAGACAGATCCATTCGATTAGTGAACGGATCCTTGGCACTTATCTGGGACGATCTGCGGAGCCTGTGCCTCTTCAGCTACCACCGCTTGAGAGACTTACTCTTGATTGTAACGAGGATTGTGGAACTTCTGGGACGCAGGGGGTGGGAAGCCCTCAAATATTGGTGGAATCTCCTACAGTATTGGAGTCAGGAACTAAAGAATAGTGCTGTTAGCTTGCTCAATGCCACAGCCATAGCAGTAGCTGAGGGGACAGATAGGGTTATAGAAGTAGTACAAGGAGCTTGT",
            'Int/RNAse H/RTend':	"GAAACATGGGAAACATGGTGGACAGAGTATTGGCAAGCCACCTGGATTCCTGAGTGGGAGTTTGTTAATACCCCTCCCTTAGTGAAATTATGGTACCAGTTAGAGAAAGAACCCATAGTAGGAGCAGAAACCTTCTATGTAGATGGGGCAGCTAACAGGGAGACTAAATTAGGAAAAGCAGGATATGTTACTAATAGAGGAAGACAAAAAGTTGTCACCCTAACTGACACAACAAATCAGAAGACTGAGTTACAAGCAATTTATCTAGCTTTGCAGGATTCGGGATTAGAAGTAAACATAGTAACAGACTCACAATATGCATTAGGAATCATTCAAGCACAACCAGATCAAAGTGAATCAGAGTTAGTCAATCAAATAATAGAGCAGTTAATAAAAAAGGAAAAGGTCTATCTGGCATGGGTACCAGCACACAAAGGAATTGGAGGAAATGAACAAGTAGATAAATTAGTCAGTGCTGGAATCAGGAAAGTACTATTTTTAGATGGAATAGATAAGGCCCAAGATGAACATGAGAAATATCACAGTAATTGGAGAGCAATGGCTAGTGATTTTAACCTGCCACCTGTAGTAGCAAAAGAAATAGTAGCCAGCTGTGATAAATGTCAGCTAAAAGGAGAAGCCATGCATGGACAAGTAGACTGTAGTCCAGGAATATGGCAACTAGATTGTACACATTTAGAAGGAAAAGTTATCCTGGTAGCAGTTCATGTAGCCAGTGGATATATAGAAGCAGAAGTTATTCCAGCAGAAACAGGGCAGGAAACAGCATATTTTCTTTTAAAATTAGCAGGAAGATGGCCAGTAAAAACAATACATACTGACAATGGCAGCAATTTCACCGGTGCTACGGTTAGGGCCGCCTGTTGGTGGGCGGGAATCAAGCAGGAATTTGGAATTCCCTACAATCCCCAAAGTCAAGGAGTAGTAGAATCTATGAATAAAGAATTAAAGAAAATTATAGGACAGGTAAGAGATCAGGCTGAACATCTTAAGACAGCAGTACAAATGGCAGTATTCATCCACAATTTTAAAAGAAAAGGGGGGATTGGGGGGTACAGTGCAGGGGAAAGAATAGTAGACATAATAGCAACAGACATACAAACTAAAGAATTACAAAAACAAATTACAAAAATTCAAAATTTTCGGGTTTATTACAGGGACAGCAGAAATCCACTTTGGAAAGGACCAGCAAAGCTCCTCTGGAAAGGTGAAGGGGCAGTAGTAATACAAGATAATAGTGACATAAAAGTAGTGCCAAGAAGAAAAGCAAAGATCATTAGGGATTATGGAAAACAGATGGCAGGTGATGATTGTGTGGCAAGTAGACAGGATGAGGATGAAACATGGGAAACATGGTGGACAGAGTATTGGCAAGCCACCTGGATTCCTGAGTGGGAGTTTGTTAATACCCCTCCCTTAGTGAAATTATGGTACCAGTTAGAGAAAGAACCCATAGTAGGAGCAGAAACCTTCTATGTAGATGGGGCAGCTAACAGGGAGACTAAATTAGGAAAAGCAGGATATGTTACTAATAGAGGAAGACAAAAAGTTGTCACCCTAACTGACACAACAAATCAGAAGACTGAGTTACAAGCAATTTATCTAGCTTTGCAGGATTCGGGATTAGAAGTAAACATAGTAACAGACTCACAATATGCATTAGGAATCATTCAAGCACAACCAGATCAAAGTGAATCAGAGTTAGTCAATCAAATAATAGAGCAGTTAATAAAAAAGGAAAAGGTCTATCTGGCATGGGTACCAGCACACAAAGGAATTGGAGGAAATGAACAAGTAGATAAATTAGTCAGTGCTGGAATCAGGAAAGTACTATTTTTAGATGGAATAGATAAGGCCCAAGATGAACATGAGAAATATCACAGTAATTGGAGAGCAATGGCTAGTGATTTTAACCTGCCACCTGTAGTAGCAAAAGAAATAGTAGCCAGCTGTGATAAATGTCAGCTAAAAGGAGAAGCCATGCATGGACAAGTAGACTGTAGTCCAGGAATATGGCAACTAGATTGTACACATTTAGAAGGAAAAGTTATCCTGGTAGCAGTTCATGTAGCCAGTGGATATATAGAAGCAGAAGTTATTCCAGCAGAAACAGGGCAGGAAACAGCATATTTTCTTTTAAAATTAGCAGGAAGATGGCCAGTAAAAACAATACATACTGACAATGGCAGCAATTTCACCGGTGCTACGGTTAGGGCCGCCTGTTGGTGGGCGGGAATCAAGCAGGAATTTGGAATTCCCTACAATCCCCAAAGTCAAGGAGTAGTAGAATCTATGAATAAAGAATTAAAGAAAATTATAGGACAGGTAAGAGATCAGGCTGAACATCTTAAGACAGCAGTACAAATGGCAGTATTCATCCACAATTTTAAAAGAAAAGGGGGGATTGGGGGGTACAGTGCAGGGGAAAGAATAGTAGACATAATAGCAACAGACATACAAACTAAAGAATTACAAAAACAAATTACAAAAATTCAAAATTTTCGGGTTTATTACAGGGACAGCAGAAATCCACTTTGGAAAGGACCAGCAAAGCTCCTCTGGAAAGGTGAAGGGGCAGTAGTAATACAAGATAATAGTGACATAAAAGTAGTGCCAAGAAGAAAAGCAAAGATCATTAGGGATTATGGAAAACAGATGGCAGGTGATGATTGTGTGGCAAGTAGACAGGATGAGGAT",
            'Int clinical':			"TTTTTAGATGGAATAGATAAGGCCCAAGATGAACATGAGAAATATCACAGTAATTGGAGAGCAATGGCTAGTGATTTTAACCTGCCACCTGTAGTAGCAAAAGAAATAGTAGCCAGCTGTGATAAATGTCAGCTAAAAGGAGAAGCCATGCATGGACAAGTAGACTGTAGTCCAGGAATATGGCAACTAGATTGTACACATTTAGAAGGAAAAGTTATCCTGGTAGCAGTTCATGTAGCCAGTGGATATATAGAAGCAGAAGTTATTCCAGCAGAAACAGGGCAGGAAACAGCATATTTTCTTTTAAAATTAGCAGGAAGATGGCCAGTAAAAACAATACATACTGACAATGGCAGCAATTTCACCGGTGCTACGGTTAGGGCCGCCTGTTGGTGGGCGGGAATCAAGCAGGAATTTGGAATTCCCTACAATCCCCAAAGTCAAGGAGTAGTAGAATCTATGAATAAAGAATTAAAGAAAATTATAGGACAGGTAAGAGATCAGGCTGAACATCTTAAGACAGCAGTACAAATGGCAGTATTCATCCACAATTTTAAAAGAAAAGGGGGGATTGGGGGGTACAGTGCAGGGGAAAGAATAGTAGACATAATAGCAACAGACATACAAACTAAAGAATTACAAAAACAAATTACAAAAATTCAAAATTTTCGGGTTTATTACAGGGACAGCAGAAATCCACTTTGGAAAGGACCAGCAAAGCTCCTCTGGAAAGGTGAAGGGGCAGTAGTAATACAAGATAATAGTGACATAAAAGTAGTGCCAAGAAGAAAAGCAAAGATCATTAGGGATTATGGAAAACAGATGGCAGGTGATGATTGTGTGGCAAGTAGACAGGATGAGGATATCAGGAAAGTACTATTTTTAGATGGAATAGATAAGGCCCAAGATGAACATGAGAAATATCACAGTAATTGGAGAGCAATGGCTAGTGATTTTAACCTGCCACCTGTAGTAGCAAAAGAAATAGTAGCCAGCTGTGATAAATGTCAGCTAAAAGGAGAAGCCATGCATGGACAAGTAGACTGTAGTCCAGGAATATGGCAACTAGATTGTACACATTTAGAAGGAAAAGTTATCCTGGTAGCAGTTCATGTAGCCAGTGGATATATAGAAGCAGAAGTTATTCCAGCAGAAACAGGGCAGGAAACAGCATATTTTCTTTTAAAATTAGCAGGAAGATGGCCAGTAAAAACAATACATACTGACAATGGCAGCAATTTCACCGGTGCTACGGTTAGGGCCGCCTGTTGGTGGGCGGGAATCAAGCAGGAATTTGGAATTCCCTACAATCCCCAAAGTCAAGGAGTAGTAGAATCTATGAATAAAGAATTAAAGAAAATTATAGGACAGGTAAGAGATCAGGCTGAACATCTTAAGACAGCAGTACAAATGGCAGTATTCATCCACAATTTTAAAAGAAAAGGGGGGATTGGGGGGTACAGTGCAGGGGAAAGAATAGTAGACATAATAGCAACAGACATACAAACTAAAGAATTACAAAAACAAATTACAAAAATTCAAAATTTTCGGGTTTATTACAGGGACAGCAGAAATCCACTTTGGAAAGGACCAGCAAAGCTCCTCTGGAAAGGTGAAGGGGCAGTAGTAATACAAGATAATAGTGACATAAAAGTAGTGCCAAGAAGAAAAGCAAAGATCATTAGGGATTATGGAAAACAGATGGCAGGTGATGATTGTGTGGCAAGTAGACAGGATGAGGAT",
            'Gag':					"ATGGGTGCGAGAGCGTCAGTATTAAGCGGGGGAGAATTAGATCGATGGGAAAAAATTCGGTTAAGGCCAGGGGGAAAGAAAAAATATAAATTAAAACATATAGTATGGGCAAGCAGGGAGCTAGAACGATTCGCAGTTAATCCTGGCCTGTTAGAAACATCAGAAGGCTGTAGACAAATACTGGGACAGCTACAACCATCCCTTCAGACAGGATCAGAAGAACTTAGATCATTATATAATACAGTAGCAACCCTCTATTGTGTGCATCAAAGGATAGAGATAAAAGACACCAAGGAAGCTTTAGACAAGATAGAGGAAGAGCAAAACAAAAGTAAGAAAAAAGCACAGCAAGCAGCAGCTGACACAGGACACAGCAATCAGGTCAGCCAAAATTACCCTATAGTGCAGAACATCCAGGGGCAAATGGTACATCAGGCCATATCACCTAGAACTTTAAATGCATGGGTAAAAGTAGTAGAAGAGAAGGCTTTCAGCCCAGAAGTGATACCCATGTTTTCAGCATTATCAGAAGGAGCCACCCCACAAGATTTAAACACCATGCTAAACACAGTGGGGGGACATCAAGCAGCCATGCAAATGTTAAAAGAGACCATCAATGAGGAAGCTGCAGAATGGGATAGAGTGCATCCAGTGCATGCAGGGCCTATTGCACCAGGCCAGATGAGAGAACCAAGGGGAAGTGACATAGCAGGAACTACTAGTACCCTTCAGGAACAAATAGGATGGATGACAAATAATCCACCTATCCCAGTAGGAGAAATTTATAAAAGATGGATAATCCTGGGATTAAATAAAATAGTAAGAATGTATAGCCCTACCAGCATTCTGGACATAAGACAAGGACCAAAGGAACCCTTTAGAGACTATGTAGACCGGTTCTATAAAACTCTAAGAGCCGAGCAAGCTTCACAGGAGGTAAAAAATTGGATGACAGAAACCTTGTTGGTCCAAAATGCGAACCCAGATTGTAAGACTATTTTAAAAGCATTGGGACCAGCGGCTACACTAGAAGAAATGATGACAGCATGTCAGGGAGTAGGAGGACCCGGCCATAAGGCAAGAGTTTTGGCTGAAGCAATGAGCCAAGTAACAAATTCAGCTACCATAATGATGCAGAGAGGCAATTTTAGGAACCAAAGAAAGATTGTTAAGTGTTTCAATTGTGGCAAAGAAGGGCACACAGCCAGAAATTGCAGGGCCCCTAGGAAAAAGGGCTGTTGGAAATGTGGAAAGGAAGGACACCAAATGAAAGATTGTACTGAGAGACAGGCTAATTTTTTAGGGAAGATCTGGCCTTCCTACAAGGGAAGGCCAGGGAATTTTCTTCAGAGCAGACCAGAGCCAACAGCCCCACCAGAAGAGAGCTTCAGGTCTGGGGTAGAGACAACAACTCCCCCTCAGAAGCAGGAGCCGATAGACAAGGAACTGTATCCTTTAACTTCCCTCAGGTCACTCTTTGGCAACGACCCCTCGTCACAA",
            'HLA-A, clinical':		"GCTCCCACTCCATGAGGTATTTCTTCACATCCGTGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCATCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGCCAGAAGATGGAGCCGCGGGCGCCGTGGATAGAGCAGGAGGGGCCGGAGTATTGGGACCAGGAGACACGGAATATGAAGGCCCACTCACAGACTGACCGAGCGAACCTGGGGACCCTGCGCGGCTACTACAACCAGAGCGAGGACGGTGAGTGACCCCGGCCCGGGGCGCAGGTCACGACCCCTCATCCCCCACGGACGGGCCAGGTCGCCCACAGTCTCCGGGTCCGAGATCCACCCCGAAGCCGCGGGACTCCGAGACCCTTGTCCCGGGAGAGGCCCAGGCGCCTTTACCCGGTTTCATTTTCAGTTTAGGCCAAAAATCCCCCCGGGTTGGTCGGGGCGGGGCGGGGCTCGGGGGACTGGGCTGACCGCGGGGTCGGGGCCAGGTTCTCACACCATCCAGATAATGTATGGCTGCGACGTGGGGCCGGACGGGCGCTTCCTCCGCGGGTACCGGCAGGACGCCTACGACGGCAAGGATTACATCGCCCTGAACGAGGACCTGCGCTCTTGGACCGCGGCGGACATGGCAGCTCAGATCACCAAGCGCAAGTGGGAGGCGGTCCATGCGGCGGAGCAGCGGAGAGTCTACCTGGAGGGCCGGTGCGTGGACGGGCTCCGCAGATACCTGGAGAACGGGAAGGAGACGCTGCAGCGCACGG",
            'HLA-Ba, clinical':		"CCCACTCCATGAGGTATTTCTACACCTCCGTGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCATCTCAGTGGGCTACGTGGACGACACCCAGTTCGTGAGGTTCGACAGCGACGCCGCGAGTCCGAGAGAGGAGCCGCGGGCGCCGTGGATAGAGCAGGAGGGGCCGGAGTATTGGGACCGGAACACACAGATCTACAAGGCCCAGGCACAGACTGACCGAGAGAGCCTGCGGAACCTGCGCGGCTACTACAACCAGAGCGAGGCCG",
            'HLA-Bb, clinical':		"GTCTCACACCCTCCAGAGCATGTACGGCTGCGACGTGGGGCCGGACGGGCGCCTCCTCCGCGGGCATGACCAGTACGCCTACGACGGCAAGGATTACATCGCCCTGAACGAGGACCTGCGCTCCTGGACCGCCGCGGACACGGCGGCTCAGATCACCCAGCGCAAGTGGGAGGCGGCCCGTGAGGCGGAGCAGCGGAGAGCCTACCTGGAGGGCGAGTGCGTGGAGTGGCTCCGCAGATACCTGGAGAACGGGAAGGACAAGCTGGAGCGCGCTG",
            'HLA-Ca, clinical':		"GCTCCCACTCCATGAAGTATTTCTTCACATCCGTGTCCCGGCCTGGCCGCGGAGAGCCCCGCTTCATCTCAGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGTCCGAGAGGGGAGCCGCGGGCGCCGTGGGTGGAGCAGGAGGGGCCGGAGTATTGGGACCGGGAGACACAGAAGTACAAGCGCCAGGCACAGACTGACCGAGTGAGCCTGCGGAACCTGCGCGGCTACTACAACCAGAGCGAGGCCG",
            'HLA-Cb, clinical':		"GTCTCACACCCTCCAGTGGATGTGTGGCTGCGACCTGGGGCCCGACGGGCGCCTCCTCCGCGGGTATGACCAGTACGCCTACGACGGCAAGGATTACATCGCCCTGAACGAGGACCTGCGCTCCTGGACCGCCGCGGACACCGCGGCTCAGATCACCCAGCGCAAGTGGGAGGCGGCCCGTGAGGCGGAGCAGCGGAGAGCCTACCTGGAGGGCACGTGCGTGGAGTGGCTCCGCAGATACCTGGAGAACGGGAAGGAGACGCTGCAGCGCGCGG",
            'Nef':					"ATGGGTGGCAAGTGGTCAAAAAGTAGTGTGATTGGATGGCCTACTGTAAGGGAAAGAATGAGACGAGCTGAGCCAGCAGCAGATAGGGTGGGAGCAGCATCTCGAGACCTGGAAAAACATGGAGCAATCACAAGTAGCAATACAGCAGCTACCAATGCTGCTTGTGCCTGGCTAGAAGCACAAGAGGAGGAGGAGGTGGGTTTTCCAGTCACACCTCAGGTACCTTTAAGACCAATGACTTACAAGGCAGCTGTAGATCTTAGCCACTTTTTAAAAGAAAAGGGGGGACTGGAAGGGCTAATTCACTCCCAAAGAAGACAAGATATCCTTGATCTGTGGATCTACCACACACAAGGCTACTTCCCTGATTAGCAGAACTACACACCAGGGCCAGGGGTCAGATATCCACTGACCTTTGGATGGTGCTACAAGCTAGTACCAGTTGAGCCAGATAAGATAGAAGAGGCCAATAAAGGAGAGAACACCAGCTTGTTACACCCTGTGAGCCTGCATGGGATGGATGACCCGGAGAGAGAAGTGTTAGAGTGGAGGTTTGACAGCCGCCTAGCATTTCATCACGTGGCCCGAGAGCTGCATCCGGAGTACTTCAAGAACTGC",
            'Gag/Pol':				"ATGGGTGCGAGAGCGTCAGTATTAAGCGGGGGAGAATTAGATCGATGGGAAAAAATTCGGTTAAGGCCAGGGGGAAAGAAAAAATATAAATTAAAACATATAGTATGGGCAAGCAGGGAGCTAGAACGATTCGCAGTTAATCCTGGCCTGTTAGAAACATCAGAAGGCTGTAGACAAATACTGGGACAGCTACAACCATCCCTTCAGACAGGATCAGAAGAACTTAGATCATTATATAATACAGTAGCAACCCTCTATTGTGTGCATCAAAGGATAGAGATAAAAGACACCAAGGAAGCTTTAGACAAGATAGAGGAAGAGCAAAACAAAAGTAAGAAAAAAGCACAGCAAGCAGCAGCTGACACAGGACACAGCAATCAGGTCAGCCAAAATTACCCTATAGTGCAGAACATCCAGGGGCAAATGGTACATCAGGCCATATCACCTAGAACTTTAAATGCATGGGTAAAAGTAGTAGAAGAGAAGGCTTTCAGCCCAGAAGTGATACCCATGTTTTCAGCATTATCAGAAGGAGCCACCCCACAAGATTTAAACACCATGCTAAACACAGTGGGGGGACATCAAGCAGCCATGCAAATGTTAAAAGAGACCATCAATGAGGAAGCTGCAGAATGGGATAGAGTGCATCCAGTGCATGCAGGGCCTATTGCACCAGGCCAGATGAGAGAACCAAGGGGAAGTGACATAGCAGGAACTACTAGTACCCTTCAGGAACAAATAGGATGGATGACAAATAATCCACCTATCCCAGTAGGAGAAATTTATAAAAGATGGATAATCCTGGGATTAAATAAAATAGTAAGAATGTATAGCCCTACCAGCATTCTGGACATAAGACAAGGACCAAAGGAACCCTTTAGAGACTATGTAGACCGGTTCTATAAAACTCTAAGAGCCGAGCAAGCTTCACAGGAGGTAAAAAATTGGATGACAGAAACCTTGTTGGTCCAAAATGCGAACCCAGATTGTAAGACTATTTTAAAAGCATTGGGACCAGCGGCTACACTAGAAGAAATGATGACAGCATGTCAGGGAGTAGGAGGACCCGGCCATAAGGCAAGAGTTTTGGCTGAAGCAATGAGCCAAGTAACAAATTCAGCTACCATAATGATGCAGAGAGGCAATTTTAGGAACCAAAGAAAGATTGTTAAGTGTTTCAATTGTGGCAAAGAAGGGCACACAGCCAGAAATTGCAGGGCCCCTAGGAAAAAGGGCTGTTGGAAATGTGGAAAGGAAGGACACCAAATGAAAGATTGTACTGAGAGACAGGCTAATTTTTTAGGGAAGATCTGGCCTTCCTACAAGGGAAGGCCAGGGAATTTTCTTCAGAGCAGACCAGAGCCAACAGCCCCACCAGAAGAGAGCTTCAGGTCTGGGGTAGAGACAACAACTCCCCCTCAGAAGCAGGAGCCGATAGACAAGGAACTGTATCCTTTAACTTCCCTCAGGTCACTCTTTGGCAACGACCCCTCGTCACAATAAAGATAGGGGGGCAACTAAAGGAAGCTCTATTAGATACAGGAGCAGATGATACAGTATTAGAAGAAATGAGTTTGCCAGGAAGATGGAAACCAAAAATGATAGGGGGAATTGGAGGTTTTATCAAAGTAAGACAGTATGATCAGATACTCATAGAAATCTGTGGACATAAAGCTATAGGTACAGTATTAGTAGGACCTACACCTGTCAACATAATTGGAAGAAATCTGTTGACTCAGATTGGTTGCACTTTAAATTTT",
            'Vif/Vpr/Vpu':			"ATGGAAAACAGATGGCAGGTGATGATTGTGTGGCAAGTAGACAGGATGAGGATTAGAACATGGAAAAGTTTAGTAAAACACCATATGTATGTTTCAGGGAAAGCTAGGGGATGGTTTTATAGACATCACTATGAAAGCCCTCATCCAAGAATAAGTTCAGAAGTACACATCCCACTAGGGGATGCTAGATTGGTAATAACAACATATTGGGGTCTGCATACAGGAGAAAGAGACTGGCATTTGGGTCAGGGAGTCTCCATAGAATGGAGGAAAAAGAGATATAGCACACAAGTAGACCCTGAACTAGCAGACCAACTAATTCATCTGTATTACTTTGACTGTTTTTCAGACTCTGCTATAAGAAAGGCCTTATTAGGACACATAGTTAGCCCTAGGTGTGAATATCAAGCAGGACATAACAAGGTAGGATCTCTACAATACTTGGCACTAGCAGCATTAATAACACCAAAAAAGATAAAGCCACCTTTGCCTAGTGTTACGAAACTGACAGAGGATAGATGGAACAAGCCCCAGAAGACCAAGGGCCACAGAGGGAGCCACACAATGAATGGACACTAGAGCTTTTAGAGGAGCTTAAGAATGAAGCTGTTAGACATTTTCCTAGGATTTGGCTCCATGGCTTAGGGCAACATATCTATGAAACTTATGGGGATACTTGGGCAGGAGTGGAAGCCATAATAAGAATTCTGCAACAACTGCTGTTTATCCATTTTCAGAATTGGGTGTCGACATAGCAGAATAGGCGTTACTCGACAGAGGAGAGCAAGAAATGGAGCCAGTAGATCCTAGACTAGAGCCCTGGAAGCATCCAGGAAGTCAGCCTAAAACTGCTTGTACCAATTGCTATTGTAAAAAGTGTTGCTTTCATTGCCAAGTTTGTTTCATAACAAAAGCCTTAGGCATCTCCTATGGCAGGAAGAAGCGGAGACAGCGACGAAGAGCTCATCAGAACAGTCAGACTCATCAAGCTTCTCTATCAAAGCAGTAAGTAGTACATGTAACGCAACCTATACCAATAGTAGCAATAGTAGCATTAGTAGTAGCAATAATAATAGCAATAGTTGTGTGGTCCATAGTAATCATAGAATATAGGAAAATATTAAGACAAAGAAAAATAGACAGGTTAATTGATAGACTAATAGAAAGAGCAGAAGACAGTGGCAATGAGAGTGAAGGAGAAATATCAGCACTTGTGGAGATGGGGGTGGAGATGGGGCACCATGCTCCTTGGGATGTTGATGATCTG",
            'ABI Standard':			"TATGATTACTGTTAATGTTGCTACTACTGCTGACAATGCTGCTGCTGCTTCTCCTCACTGTCTCCACTTCCTTGAACAATGCGCCGTCATGCTTCTTTTGCCTCCCGCTGCTCCAGAAAGCTAGGCCGCAGATCAGAACCACCACAGTCAATATCACCACCTTCCTCTTATAGATTCGGAATCTCATGATAGGGGCTCAGCCTCTGTGCGAGTGGAGAGAAGTTTGCAGGCGAGCTGAGGAGCAATTGCAGGTGATATGATGTGCTCGGCTCAAGAAGCGGGCCCGGAGAGGAAGAAGTCGTGCCGGGGCTAATTATTGGCAAAACGAGCTCTTGTTGTAAACATTGATCCAACTGGAATGTCACTAATGGCGAATCAATATTCCATAAGGCATGATGGTTGCTCAGAGGCAGGAGAAGAGCAACGAATACGATCCTATAAAAGATAAAACATAAATAAACAGTCTTGATTATATTCTGGGTATTAAAGCCACAATCAGAACAAATATATGCTTTGTATCTTTTCTTGCCTTCTTCATTACCAACTGCTTCCGCGGCCACATTAAGAGAACTTGTGGTAAGATAAGAAGATATTTTATTCGTTCTGCTGACTTGCTGGATGTCGGGAAATATTCTGCATTTGATAAGAGGCGGTTAATTGCAGATATAATTGGTAGTGAAAAGGGTCGTTGCTATGGTCACCGTGAAGCGAGTACAGCAGCACAAGAATGTGTGCCGTTCTCAGTTAATATTGTTTGAATATGGTAACCTGTTTTAGTCGGTTTAAAGGTAAGAAGATCTAACCAAAAACAACACTGCAGTGACTGATTGTAGTATTTATTTTTTTACTTAATCTTAATTTTGGTGTAAA",
            'gp160':				"ATGAGAGTGAAGGAGAAATATCAGCACTTGTGGAGATGGGGGTGGAGATGGGGCACCATGCTCCTTGGGATGTTGATGATCTGTAGTGCTACAGAAAAATTGTGGGTCACAGTCTATTATGGGGTACCTGTGTGGAAGGAAGCAACCACCACTCTATTTTGTGCATCAGATGCTAAAGCATATGATACAGAGGTACATAATGTTTGGGCCACACATGCCTGTGTACCCACAGACCCCAACCCACAAGAAGTAGTATTGGTAAATGTGACAGAAAATTTTAACATGTGGAAAAATGACATGGTAGAACAGATGCATGAGGATATAATCAGTTTATGGGATCAAAGCCTAAAGCCATGTGTAAAATTAACCCCACTCTGTGTTAGTTTAAAGTGCACTGATTTGAAGAATGATACTAATACCAATAGTAGTAGCGGGAGAATGATAATGGAGAAAGGAGAGATAAAAAACTGCTCTTTCAATATCAGCACAAGCATAAGAGGTAAGGTGCAGAAAGAATATGCATTTTTTTATAAACTTGATATAATACCAATAGATAATGATACTACCAGCTATAAGTTGACAAGTTGTAACACCTCAGTCATTACACAGGCCTGTCCAAAGGTATCCTTTGAGCCAATTCCCATACATTATTGTGCCCCGGCTGGTTTTGCGATTCTAAAATGTAATAATAAGACGTTCAATGGAACAGGACCATGTACAAATGTCAGCACAGTACAATGTACACATGGAATTAGGCCAGTAGTATCAACTCAACTGCTGTTAAATGGCAGTCTAGCAGAAGAAGAGGTAGTAATTAGATCTGTCAATTTCACGGACAATGCTAAAACCATAATAGTACAGCTGAACACATCTGTAGAAATTAATTGTACAAGACCCAACAACAATACAAGAAAAAGAATCCGTATCCAGAGAGGACCAGGGAGAGCATTTGTTACAATAGGAAAAATAGGAAATATGAGACAAGCACATTGTAACATTAGTAGAGCAAAATGGAATAACACTTTAAAACAGATAGCTAGCAAATTAAGAGAACAATTTGGAAATAATAAAACAATAATCTTTAAGCAATCCTCAGGAGGGGACCCAGAAATTGTAACGCACAGTTTTAATTGTGGAGGGGAATTTTTCTACTGTAATTCAACACAACTGTTTAATAGTACTTGGTTTAATAGTACTTGGAGTACTGAAGGGTCAAATAACACTGAAGGAAGTGACACAATCACCCTCCCATGCAGAATAAAACAAATTATAAACATGTGGCAGAAAGTAGGAAAAGCAATGTATGCCCCTCCCATCAGTGGACAAATTAGATGTTCATCAAATATTACAGGGCTGCTATTAACAAGAGATGGTGGTAATAGCAACAATGAGTCCGAGATCTTCAGACCTGGAGGAGGAGATATGAGGGACAATTGGAGAAGTGAATTATATAAATATAAAGTAGTAAAAATTGAACCATTAGGAGTAGCACCCACCAAGGCAAAGAGAAGAGTGGTGCAGAGAGAAAAAAGAGCAGTGGGAATAGGAGCTTTGTTCCTTGGGTTCTTGGGAGCAGCAGGAAGCACTATGGGCGCAGCCTCAATGACGCTGACGGTACAGGCCAGACAATTATTGTCTGGTATAGTGCAGCAGCAGAACAATTTGCTGAGGGCTATTGAGGCGCAACAGCATCTGTTGCAACTCACAGTCTGGGGCATCAAGCAGCTCCAGGCAAGAATCCTGGCTGTGGAAAGATACCTAAAGGATCAACAGCTCCTGGGGATTTGGGGTTGCTCTGGAAAACTCATTTGCACCACTGCTGTGCCTTGGAATGCTAGTTGGAGTAATAAATCTCTGGAACAGATTTGGAATCACACGACCTGGATGGAGTGGGACAGAGAAATTAACAATTACACAAGCTTAATACACTCCTTAATTGAAGAATCGCAAAACCAGCAAGAAAAGAATGAACAAGAATTATTGGAATTAGATAAATGGGCAAGTTTGTGGAATTGGTTTAACATAACAAATTGGCTGTGGTATATAAAATTATTCATAATGATAGTAGGAGGCTTGGTAGGTTTAAGAATAGTTTTTGCTGTACTTTCTATAGTGAATAGAGTTAGGCAGGGATATTCACCATTATCGTTTCAGACCCACCTCCCAACCCCGAGGGGACCCGACAGGCCCGAAGGAATAGAAGAAGAAGGTGGAGAGAGAGACAGAGACAGATCCATTCGATTAGTGAACGGATCCTTGGCACTTATCTGGGACGATCTGCGGAGCCTGTGCCTCTTCAGCTACCACCGCTTGAGAGACTTACTCTTGATTGTAACGAGGATTGTGGAACTTCTGGGACGCAGGGGGTGGGAAGCCCTCAAATATTGGTGGAATCTCCTACAGTATTGGAGTCAGGAACTAAAGAATAGTGCTGTTAGCTTGCTCAATGCCACAGCCATAGCAGTAGCTGAGGGGACAGATAGGGTTATAGAAGTAGTACAAGGAGCTTGTAGAGCTATTCGCCACATACCTAGAAGAATAAGACAGGGCTTGGAAAGGATTTTGCTATAA",
            'V3, clinical':			"TGTACAAGACCCAACAACAATACAAGAAAAAGTATACATATAGGACCAGGGAGAGCATTTTATGCAACAGGAGAAATAATAGGAGATATAAGACAAGCACATTGT",
            'V3, extended':			"AATTTCACAGACAATACCAAAACCATAATAGTACAGCTGAAGGAATCTGTAGAAATTAATTGTACAAGACCCAACAACAATACAAGAAAAAGTATACATATAGGACCAGGGAGAGCATTTTATGCAACAGGAGAAATAATAGGAGATATAAGACAAGCACATTGTAACCTTAGTAGAGCAAAATGGAATGACACTTTAAACCAGATAGTT"}


scoreMatrixGonnet = """\
{{2.4,-0.6,-0.3,-0.3,0.5,0.0,-0.2,0.5,-0.8,-0.8,-1.2,-0.4,-0.7,-2.3,0.3,1.1,0.6,-3.6,-2.2,0.1,-5.0,-8.0},\
{-0.6,4.7,0.3,-0.3,-2.2,0.4,1.5,-1.0,0.6,-2.4,-2.2,2.7,-1.7,-3.2,-0.9,-0.2,-0.2,-1.6,-1.8,-2.0,-5.0,-8.0},\
{-0.3,0.3,3.8,2.2,-1.8,0.9,0.7,0.4,1.2,-2.8,-3.0,0.8,-2.2,-3.1,-0.9,0.9,0.5,-3.6,-1.4,-2.2,-5.0,-8.0},\
{-0.3,-0.3,2.2,4.7,-3.2,2.7,0.9,0.1,0.4,-3.8,-4.0,0.5,-3.0,-4.5,-0.7,0.5,0.0,-5.2,-2.8,-2.9,-5.0,-8.0},\
{0.5,-2.2,-1.8,-3.2,11.5,-3.0,-2.4,-2.0,-1.3,-1.1,-1.5,-2.8,-0.9,-0.8,-3.1,0.1,-0.5,-1.0,-0.5,0.0,-5.0,-8.0},\
{0.0,0.4,0.9,2.7,-3.0,3.6,1.7,-0.8,0.4,-2.7,-2.8,1.2,-2.0,-3.9,-0.5,0.2,-0.1,-4.3,-2.7,-1.9,-5.0,-8.0},\
{-0.2,1.5,0.7,0.9,-2.4,1.7,2.7,-1.0,1.2,-1.9,-1.6,1.5,-1.0,-2.6,-0.2,0.2,0.0,-2.7,-1.7,-1.5,-5.0,-8.0},\
{0.5,-1.0,0.4,0.1,-2.0,-0.8,-1.0,6.6,-1.4,-4.5,-4.4,-1.1,-3.5,-5.2,-1.6,0.4,-1.1,-4.0,-4.0,-3.3,-5.0,-8.0},\
{-0.8,0.6,1.2,0.4,-1.3,0.4,1.2,-1.4,6.0,-2.2,-1.9,0.6,-1.3,-0.1,-1.1,-0.2,-0.3,-0.8,2.2,-2.0,-5.0,-8.0},\
{-0.8,-2.4,-2.8,-3.8,-1.1,-2.7,-1.9,-4.5,-2.2,4.0,2.8,-2.1,2.5,1.0,-2.6,-1.8,-0.6,-1.8,-0.7,3.1,-5.0,-8.0},\
{-1.2,-2.2,-3.0,-4.0,-1.5,-2.8,-1.6,-4.4,-1.9,2.8,4.0,-2.1,2.8,2.0,-2.3,-2.1,-1.3,-0.7,0.0,1.8,-5.0,-8.0},\
{-0.4,2.7,0.8,0.5,-2.8,1.2,1.5,-1.1,0.6,-2.1,-2.1,3.2,-1.4,-3.3,-0.6,0.1,0.1,-3.5,-2.1,-1.7,-5.0,-8.0},\
{-0.7,-1.7,-2.2,-3.0,-0.9,-2.0,-1.0,-3.5,-1.3,2.5,2.8,-1.4,4.3,1.6,-2.4,-1.4,-0.6,-1.0,-0.2,1.6,-5.0,-8.0},\
{-2.3,-3.2,-3.1,-4.5,-0.8,-3.9,-2.6,-5.2,-0.1,1.0,2.0,-3.3,1.6,7.0,-3.8,-2.8,-2.2,3.6,5.1,0.1,-5.0,-8.0},\
{0.3,-0.9,-0.9,-0.7,-3.1,-0.5,-0.2,-1.6,-1.1,-2.6,-2.3,-0.6,-2.4,-3.8,7.6,0.4,0.1,-5.0,-3.1,-1.8,-5.0,-8.0},\
{1.1,-0.2,0.9,0.5,0.1,0.2,0.2,0.4,-0.2,-1.8,-2.1,0.1,-1.4,-2.8,0.4,2.2,1.5,-3.3,-1.9,-1.0,-5.0,-8.0},\
{0.6,-0.2,0.5,0.0,-0.5,-0.1,0.0,-1.1,-0.3,-0.6,-1.3,0.1,-0.6,-2.2,0.1,1.5,2.5,-3.5,-1.9,0.0,-5.0,-8.0},\
{-3.6,-1.6,-3.6,-5.2,-1.0,-4.3,-2.7,-4.0,-0.8,-1.8,-0.7,-3.5,-1.0,3.6,-5.0,-3.3,-3.5,14.2,4.1,-2.6,-5.0,-8.0},\
{-2.2,-1.8,-1.4,-2.8,-0.5,-2.7,-1.7,-4.0,2.2,-0.7,0.0,-2.1,-0.2,5.1,-3.1,-1.9,-1.9,4.1,7.8,-1.1,-5.0,-8.0},\
{0.1,-2.0,-2.2,-2.9,0.0,-1.9,-1.5,-3.3,-2.0,3.1,1.8,-1.7,1.6,0.1,-1.8,-1.0,0.0,-2.6,-1.1,3.4,-5.0,-8.0},\
{-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,-5.0,1.0,-5.0},\
{-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,-8.0,1.0}};
"""

scoreMatrixBLOSUM = """\
{{6,-3,-4,-4,-2,-2,-2,-1,-3,-3,-3,-2,-2,-4,-2,0,-1,-5,-3,-1,-4,-2,-2,-7},\
{-3,8,-2,-4,-6,0,-2,-5,-2,-6,-4,1,-3,-5,-4,-2,-3,-5,-3,-5,-3,-1,-2,-7},\
{-4,-2,8,0,-5,-1,-2,-2,0,-6,-6,-1,-4,-5,-4,0,-1,-7,-4,-5,6,-2,-2,-7},\
{-4,-4,0,8,-6,-2,0,-3,-3,-5,-6,-2,-6,-6,-3,-1,-3,-7,-6,-6,6,0,-3,-7},\
{-2,-6,-5,-6,10,-5,-7,-5,-5,-3,-3,-6,-3,-5,-5,-2,-2,-4,-4,-2,-5,-6,-4,-7},\
{-2,0,-1,-2,-5,8,1,-4,0,-6,-4,0,-1,-6,-3,-1,-2,-3,-3,-4,-1,6,-2,-7},\
{-2,-2,-2,0,-7,1,7,-4,-1,-6,-5,0,-4,-6,-3,-1,-2,-5,-4,-4,0,6,-2,-7},\
{-1,-5,-2,-3,-5,-4,-4,7,-4,-7,-6,-3,-5,-5,-4,-2,-4,-4,-5,-6,-2,-4,-4,-7},\
{-3,-2,0,-3,-5,0,-1,-4,10,-6,-5,-2,-3,-3,-4,-2,-4,-5,0,-6,-1,-1,-3,-7},\
{-3,-6,-6,-5,-3,-6,-6,-7,-6,6,0,-5,0,-1,-5,-5,-2,-5,-3,2,-5,-6,-2,-7},\
{-3,-4,-6,-6,-3,-4,-5,-6,-5,0,6,-5,1,-1,-5,-5,-3,-3,-3,0,-6,-5,-2,-7},\
{-2,1,-1,-2,-6,0,0,-3,-2,-5,-5,7,-3,-6,-2,-1,-2,-5,-3,-4,-2,0,-2,-7},\
{-2,-3,-4,-6,-3,-1,-4,-5,-3,0,1,-3,9,-1,-5,-3,-2,-3,-3,0,-5,-2,-1,-7},\
{-4,-5,-5,-6,-5,-6,-6,-5,-3,-1,-1,-6,-1,8,-6,-4,-4,0,1,-3,-6,-6,-3,-7},\
{-2,-4,-4,-3,-5,-3,-3,-4,-4,-5,-5,-2,-5,-6,9,-2,-3,-6,-5,-4,-4,-3,-4,-7},\
{0,-2,0,-1,-2,-1,-1,-2,-2,-5,-5,-1,-3,-4,-2,7,0,-5,-3,-4,-1,-1,-2,-7},\
{-1,-3,-1,-3,-2,-2,-2,-4,-4,-2,-3,-2,-2,-4,-3,0,7,-4,-3,-1,-2,-2,-2,-7},\
{-5,-5,-7,-7,-4,-3,-5,-4,-5,-5,-3,-5,-3,0,-6,-5,-4,12,0,-6,-7,-4,-4,-7},\
{-3,-3,-4,-6,-4,-3,-4,-5,0,-3,-3,-3,-3,1,-5,-3,-3,0,9,-3,-5,-3,-2,-7},\
{-1,-5,-5,-6,-2,-4,-4,-6,-6,2,0,-4,0,-3,-4,-4,-1,-6,-3,6,-6,-4,-2,-7},\
{-4,-3,6,6,-5,-1,0,-2,-1,-5,-6,-2,-5,-6,-4,-1,-2,-7,-5,-6,7,-1,-3,-7},\
{-2,-1,-2,0,-6,6,6,-4,-1,-6,-5,0,-2,-6,-3,-1,-2,-4,-3,-4,-1,7,-2,-7},\
{-2,-2,-2,-3,-4,-2,-2,-4,-3,-2,-2,-2,-1,-3,-4,-2,-2,-4,-2,-2,-3,-2,-2,-7},\
{-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,1}};
"""

scoreMatrixHIV5 = """\
{{8,-13,-16,-8,-15,-17,-8,-7,-16,-14,-14,-17,-16,-20,-7,-7,-2,-23,-23,-4,-10,-10,-8,-24},\
{-13,8,-12,-20,-12,-6,-15,-6,-3,-11,-11,-1,-7,-21,-9,-6,-7,-10,-18,-16,-14,-8,-7,-24},\
{-16,-12,9,-1,-15,-11,-14,-12,-4,-11,-20,-4,-19,-20,-17,-2,-4,-24,-8,-18,7,-12,-7,-24},\
{-8,-20,-1,9,-22,-19,-3,-7,-8,-19,-22,-15,-22,-23,-19,-11,-13,-23,-11,-9,7,-4,-7,-24},\
{-15,-12,-15,-22,11,-23,-23,-10,-13,-19,-15,-21,-22,-3,-20,-5,-10,-7,-4,-12,-17,-23,-9,-24},\
{-17,-6,-11,-19,-23,8,-7,-17,-4,-20,-8,-4,-13,-20,-5,-15,-13,-20,-15,-20,-12,6,-8,-24},\
{-8,-15,-14,-3,-23,-7,8,-6,-15,-20,-23,-5,-14,-24,-20,-19,-13,-23,-17,-9,-5,6,-9,-24},\
{-7,-6,-12,-7,-10,-17,-6,7,-19,-20,-22,-11,-21,-13,-20,-5,-12,-9,-22,-10,-8,-7,-9,-24},\
{-16,-3,-4,-8,-13,-4,-15,-19,11,-16,-8,-14,-19,-13,-7,-12,-10,-17,-1,-22,-5,-6,-7,-24},\
{-14,-11,-11,-19,-19,-20,-20,-20,-16,7,-4,-13,-3,-6,-17,-9,-3,-22,-15,-1,-12,-20,-7,-24},\
{-14,-11,-20,-22,-15,-8,-23,-22,-8,-4,7,-16,-5,-3,-7,-10,-16,-10,-15,-8,-21,-11,-9,-24},\
{-17,-1,-4,-15,-21,-4,-5,-11,-14,-13,-16,8,-9,-19,-17,-11,-5,-20,-22,-13,-6,-5,-6,-24},\
{-16,-7,-19,-22,-22,-13,-14,-21,-19,-3,-5,-9,11,-13,-20,-18,-5,-16,-23,-4,-20,-14,-7,-24},\
{-20,-21,-20,-23,-3,-20,-24,-13,-13,-6,-3,-19,-13,10,-19,-10,-18,-10,-2,-10,-21,-22,-8,-24},\
{-7,-9,-17,-19,-20,-5,-20,-20,-7,-17,-7,-17,-20,-19,9,-5,-8,-18,-18,-20,-18,-8,-9,-24},\
{-7,-6,-2,-11,-5,-15,-19,-5,-12,-9,-10,-11,-18,-10,-5,8,-3,-19,-11,-16,-4,-17,-7,-24},\
{-2,-7,-4,-13,-10,-13,-13,-12,-10,-3,-16,-5,-5,-18,-8,-3,8,-23,-16,-10,-6,-13,-6,-24},\
{-23,-10,-24,-23,-7,-20,-23,-9,-17,-22,-10,-20,-16,-10,-18,-19,-23,10,-9,-23,-23,-21,-12,-24},\
{-23,-18,-8,-11,-4,-15,-17,-22,-1,-15,-15,-22,-23,-2,-18,-11,-16,-9,10,-18,-9,-16,-9,-24},\
{-4,-16,-18,-9,-12,-20,-9,-10,-22,-1,-8,-13,-4,-10,-20,-16,-10,-23,-18,8,-11,-11,-7,-24},\
{-10,-14,7,7,-17,-12,-5,-8,-5,-12,-21,-6,-20,-21,-18,-4,-6,-23,-9,-11,8,-6,-8,-24},\
{-10,-8,-12,-4,-23,6,6,-7,-6,-20,-11,-5,-14,-22,-8,-17,-13,-21,-16,-11,-6,7,-9,-24},\
{-8,-7,-7,-7,-9,-8,-9,-9,-7,-7,-9,-6,-7,-8,-9,-7,-6,-12,-9,-7,-8,-9,-8,-24},\
{-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,-24,1}};
"""

scoreMatrixHIV25 = """\
{{7,-7,-7,-4,-10,-11,-4,-3,-10,-6,-9,-9,-7,-13,-3,-2,1,-16,-15,0,-5,-5,-3,-17},\
{-7,7,-5,-11,-8,-2,-7,-2,0,-6,-6,2,-3,-12,-4,-2,-2,-5,-9,-10,-7,-3,-3,-17},\
{-7,-5,8,2,-9,-6,-6,-7,0,-6,-12,0,-10,-12,-9,1,0,-17,-3,-10,6,-6,-3,-17},\
{-4,-11,2,8,-14,-10,0,-2,-3,-11,-15,-7,-13,-15,-13,-5,-6,-16,-6,-5,7,0,-3,-17},\
{-10,-8,-9,-14,11,-16,-15,-5,-7,-11,-9,-13,-14,0,-12,-1,-6,-2,0,-8,-10,-16,-5,-17},\
{-11,-2,-6,-10,-16,8,-2,-10,0,-12,-4,0,-8,-12,-1,-9,-8,-14,-9,-13,-7,6,-4,-17},\
{-4,-7,-6,0,-15,-2,7,-1,-9,-12,-15,-1,-10,-17,-13,-11,-8,-15,-12,-5,0,6,-4,-17},\
{-3,-2,-7,-2,-5,-10,-1,7,-10,-11,-14,-6,-12,-9,-11,-1,-7,-5,-14,-5,-4,-3,-4,-17},\
{-10,0,0,-3,-7,0,-9,-10,10,-10,-4,-5,-10,-6,-3,-6,-6,-11,2,-14,-1,-2,-3,-17},\
{-6,-6,-6,-11,-11,-12,-12,-11,-10,7,0,-7,0,-2,-10,-4,0,-14,-9,2,-7,-12,-2,-17},\
{-9,-6,-12,-15,-9,-4,-15,-14,-4,0,6,-10,0,0,-3,-5,-8,-6,-8,-4,-13,-6,-4,-17},\
{-9,2,0,-7,-13,0,-1,-6,-5,-7,-10,7,-4,-14,-9,-5,-1,-12,-13,-9,-1,-1,-2,-17},\
{-7,-3,-10,-13,-14,-8,-10,-12,-10,0,0,-4,10,-7,-11,-9,-1,-11,-15,0,-11,-9,-3,-17},\
{-13,-12,-12,-15,0,-12,-17,-9,-6,-2,0,-14,-7,10,-11,-5,-10,-5,1,-5,-13,-14,-3,-17},\
{-3,-4,-9,-13,-12,-1,-13,-11,-3,-10,-3,-9,-11,-11,8,-1,-3,-13,-11,-12,-10,-3,-5,-17},\
{-2,-2,1,-5,-1,-9,-11,-1,-6,-4,-5,-5,-9,-5,-1,8,0,-12,-6,-9,0,-10,-3,-17},\
{1,-2,0,-6,-6,-8,-8,-7,-6,0,-8,-1,-1,-10,-3,0,7,-16,-10,-4,-2,-8,-2,-17},\
{-16,-5,-17,-16,-2,-14,-15,-5,-11,-14,-6,-12,-11,-5,-13,-12,-16,10,-4,-16,-16,-14,-8,-17},\
{-15,-9,-3,-6,0,-9,-12,-14,2,-9,-8,-13,-15,1,-11,-6,-10,-4,10,-12,-4,-10,-4,-17},\
{0,-10,-10,-5,-8,-13,-5,-5,-14,2,-4,-9,0,-5,-12,-9,-4,-16,-12,7,-7,-7,-3,-17},\
{-5,-7,6,7,-10,-7,0,-4,-1,-7,-13,-1,-11,-13,-10,0,-2,-16,-4,-7,7,-2,-4,-17},\
{-5,-3,-6,0,-16,6,6,-3,-2,-12,-6,-1,-9,-14,-3,-10,-8,-14,-10,-7,-2,6,-4,-17},\
{-3,-3,-3,-3,-5,-4,-4,-4,-3,-2,-4,-2,-3,-3,-5,-3,-2,-8,-4,-3,-4,-4,-3,-17},\
{-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,-17,1}};
"""

scoreMatrixHIV50 = """\
{{7,-5,-4,-2,-7,-8,-2,-1,-8,-2,-6,-5,-4,-9,-1,-1,2,-13,-12,1,-3,-4,-2,-13},\
{-5,6,-2,-7,-6,0,-4,0,1,-4,-4,3,-1,-9,-3,0,-1,-4,-6,-7,-4,-1,-1,-13},\
{-4,-2,7,3,-6,-3,-3,-4,0,-4,-8,0,-7,-8,-5,2,0,-13,-2,-7,6,-3,-1,-13},\
{-2,-7,3,8,-10,-6,2,-1,-1,-8,-12,-4,-10,-11,-9,-2,-4,-12,-4,-4,6,0,-2,-13},\
{-7,-6,-6,-10,11,-12,-12,-3,-4,-7,-6,-9,-10,2,-8,0,-4,0,1,-6,-7,-12,-3,-13},\
{-8,0,-3,-6,-12,7,-1,-7,1,-8,-2,0,-6,-8,0,-6,-5,-11,-6,-10,-5,5,-2,-13},\
{-2,-4,-3,2,-12,-1,7,0,-6,-8,-11,0,-7,-13,-9,-7,-5,-12,-9,-3,0,5,-2,-13},\
{-1,0,-4,-1,-3,-7,0,7,-7,-8,-10,-3,-9,-7,-8,0,-4,-3,-10,-4,-2,-1,-3,-13},\
{-8,1,0,-1,-4,1,-6,-7,9,-7,-2,-2,-7,-3,-1,-3,-4,-8,3,-10,0,-1,-1,-13},\
{-2,-4,-4,-8,-7,-8,-8,-8,-7,6,0,-5,2,0,-7,-3,0,-11,-7,3,-5,-8,-1,-13},\
{-6,-4,-8,-12,-6,-2,-11,-10,-2,0,6,-7,0,1,-1,-4,-5,-4,-5,-1,-10,-5,-3,-13},\
{-5,3,0,-4,-9,0,0,-3,-2,-5,-7,6,-3,-11,-6,-2,0,-9,-9,-6,0,0,-1,-13},\
{-4,-1,-7,-10,-10,-6,-7,-9,-7,2,0,-3,10,-4,-7,-6,0,-9,-10,1,-8,-6,-1,-13},\
{-9,-9,-8,-11,2,-8,-13,-7,-3,0,1,-11,-4,9,-7,-4,-7,-3,3,-3,-9,-10,-2,-13},\
{-1,-3,-5,-9,-8,0,-9,-8,-1,-7,-1,-6,-7,-7,8,0,-1,-11,-8,-8,-7,-2,-3,-13},\
{-1,0,2,-2,0,-6,-7,0,-3,-3,-4,-2,-6,-4,0,7,1,-9,-4,-6,0,-6,-1,-13},\
{2,-1,0,-4,-4,-5,-5,-4,-4,0,-5,0,0,-7,-1,1,6,-12,-7,-1,0,-5,-1,-13},\
{-13,-4,-13,-12,0,-11,-12,-3,-8,-11,-4,-9,-9,-3,-11,-9,-12,10,-2,-12,-12,-11,-6,-13},\
{-12,-6,-2,-4,1,-6,-9,-10,3,-7,-5,-9,-10,3,-8,-4,-7,-2,9,-9,-3,-7,-3,-13},\
{1,-7,-7,-4,-6,-10,-3,-4,-10,3,-1,-6,1,-3,-8,-6,-1,-12,-9,6,-5,-5,-1,-13},\
{-3,-4,6,6,-7,-5,0,-2,0,-5,-10,0,-8,-9,-7,0,0,-12,-3,-5,7,0,-2,-13},\
{-4,-1,-3,0,-12,5,5,-1,-1,-8,-5,0,-6,-10,-2,-6,-5,-11,-7,-5,0,6,-3,-13},\
{-2,-1,-1,-2,-3,-2,-2,-3,-1,-1,-3,-1,-1,-2,-3,-1,-1,-6,-3,-1,-2,-3,-2,-13},\
{-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,-13,1}};
"""

protAlphabet = "ARNDCQEGHILKMFPSTWYVBZX*"
gonnetAlphabet = "ARNDCEQGHILKMFPSTWYVX*"

nucAlphabet = "ACGT";

nucScoreMatrix = """\
{{5,-4,-4,-4},\
{-4,5,-4,-4},\
{-4,-4,5,-4},\
{-4,-4,-4,5}};
"""

def change_settings (hyphy, alphabet=protAlphabet, 
                            scoreMatrix=scoreMatrixHIV25,
                            gapOpen=40,
                            gapOpen2=20,
                            gapExtend=10,
                            gapExtend2=5,
                            noTerminalPenalty = 1):
    """
    Set alignment options as associative list.
    """
    hyphy.ExecuteBF("alignOptions = {};", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_CHARACTER_MAP\"]=\""+alphabet+"\";", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_SCORE_MATRIX\"] = "+scoreMatrix, False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_GAP_OPEN\"] = "+str(gapOpen)+";", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_GAP_OPEN2\"] = "+str(gapOpen2)+";", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_GAP_EXTEND\"] = "+str(gapExtend)+";", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_GAP_EXTEND2\"] = "+str(gapExtend2)+";", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_AFFINE\"] = 1;", False)
    hyphy.ExecuteBF("alignOptions [\"SEQ_ALIGN_NO_TP\"] = "+str(noTerminalPenalty)+";", False)

    return None


def align (hyphy, seqlist):
    """
    Use modified Gotoh algorithm in HyPhy to align a set of reference
    and query sequences passed as a list argument.
    """
    # convert Python list object into HyPhy string matrix
    input_string = 'inStr={'
    for ref, query in seqlist:
        input_string += '{%s,%s}' % (ref, query)
    input_string += '};'
    dump = hyphy.ExecuteBF (input_string)

    dump = hyphy.ExecuteBF ('AlignSequences(aligned, inStr, alignOptions);', False);
    aligned = hyphy.ExecuteBF ('return aligned;', False);
    exec "d = " + aligned.sData

    res = []
    # make sure we iterate through keys in numerical order
    for index in range(len(d)):
        res.append( (d[index]['2'], d[index]['1'], d[index]['0']) )

    return res



def pair_align (hyphy, refseq, query):
    """
    Returns a tuple containing aligned query and reference sequences using
    Smith-Wasserman algorithm.
    alignOptions is a persistent HyPhy object set by change_settings()
    """
    dump = hyphy.ExecuteBF ('inStr={{"'+refseq+'","'+query+'"}};', False);
    dump = hyphy.ExecuteBF ('AlignSequences(aligned, inStr, alignOptions);', False);
    aligned = hyphy.ExecuteBF ('return aligned;', False);
    exec "d = " + aligned.sData

    align_score = int(d['0']['0'])
    aligned_ref = d['0']['1']
    aligned_query = d['0']['2']

    return (aligned_query, aligned_ref, align_score)



gap_prefix = re.compile('^[-]+')
gap_suffix = re.compile('[-]+$')


def get_boundaries (str):
    # return a tuple giving indices of subsequence without gap prefix and suffix
    res = [0,len(str)]
    left = gap_prefix.findall(str)
    right = gap_suffix.findall(str)
    if left:
        res[0] = len(left[0])
    if right:
        res[1] = len(str) - len(right[0])

    return res


def apply2nuc (seq, query, ref, keepIns=False, keepDel=False):
    """
    Apply results from amino acid sequence alignment to the original
    nucleotide sequence by padding insertions with gaps, omitting
    deletions.
    """
    newseq = ''
    qpos, rpos = 0, 0	# query, reference a.a. positions

    for i in range(len(ref)):
        if query[i] == '-':
            # deletion
            if keepDel:
                newseq += '---'
            rpos += 1
        elif ref[i] == '-':
            # insertion
            if keepIns:
                newseq += seq[(3*qpos):(3*(qpos+1))]
            qpos += 1
        else:
            newseq += seq[(3*qpos):(3*(qpos+1))]
            rpos += 1
            qpos += 1

    return newseq
