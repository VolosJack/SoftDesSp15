# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Charles Long

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """

    nucleotide_comps = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    comp_nucleotide = nucleotide_comps[nucleotide]

    return comp_nucleotide
    pass

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """

    list_dna = []
    comp = ""
    reverse_comp = ""

    for i in range(len(dna)):
        comp = comp + get_complement(dna[i])


    for i in range(len(dna)):
        reverse_comp = reverse_comp + comp[len(dna)-1-i]


    return reverse_comp

    pass

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    # Added a unit test for no in-frame stop condons
    >>> rest_of_ORF("ATGTGCCC")
    'ATGTGCCC'
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """

    ORF = ''

    list_frame = [dna[i:i+3] for i in range(0, len(dna), 3)]

    for i in range(len(list_frame)):
        if list_frame[i] == "TAG" or list_frame[i] == "TGA" or list_frame[i] == "TAA":
            ORF = ''.join(list_frame[0:i])

    if ORF != '':
        return ORF
    else:
        return dna

    pass

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading ORFs in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG']

    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    >>> find_all_ORFs_oneframe("ATGCCATGTTATGAATAG")
    ['ATGCCATGTTATGAA']
    """

    # Initialize variables
    iterator = 0
    start_condon = ('ATG')
    k = []
    ORFs = [] #Output list of DNA strings

    # Create a list of condons
    list_condons = [dna[i:i+3] for i in range(0, len(dna), 3)]
    end_index = len(list_condons)

    # Split dna on start condons
    while iterator < end_index:
        if list_condons[iterator] == start_condon:
            ORFs = rest_of_ORF(''.join(list_condons[iterator:]))
            k.append(ORFs)
            jump = len([ORFs[j:j+3] for j in range(0, len(ORFs), 3)])
            iterator += jump
        else:
            iterator += 1

    return k

    pass

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG']

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """

    all_orfs = []

    # First possible frame
    all_orfs.extend(find_all_ORFs_oneframe(dna))

    # Second possible frame
    all_orfs += find_all_ORFs_oneframe(dna[1:])

    # Third possible frame
    all_orfs += find_all_ORFs_oneframe(dna[2:])

    return all_orfs

    pass

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """


    orfs = find_all_ORFs(dna)
    reverse_comp = get_reverse_complement(dna)

    reverse_orfs = find_all_ORFs(reverse_comp)

    all_orfs = orfs + reverse_orfs

    return all_orfs
    pass


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this
    all_orfs = find_all_ORFs_both_strands(dna)
    longest_ORFs = ''

    longest_ORFs = max(all_orfs)

    return longest_ORFs
    pass


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """

    all_orf_lengths = []

    for i in range (0, num_trials):
        new_string = shuffle_string(dna)
        orf_length = len(longest_ORF(new_string))
        all_orf_lengths.append(orf_length)

    return max(all_orf_lengths)

    pass

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """

    encoded_protien = ''

    list_condons = [dna[i:i+3] for i in range(0, len(dna), 3)]

    for i in list_condons:
        if len(i) == 3:
            aa = aa_table[i]
            encoded_protien += aa

    return encoded_protien

    pass

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    threshold = longest_ORF_noncoding(dna, 1500)

    no_threshold_orfs = find_all_ORFs_both_strands(dna)
    threshold_orfs =[]

    for orfs in no_threshold_orfs:
        if len(orfs) > threshold:
            threshold_orfs.append(orfs)

    aa_conversion = map(coding_strand_to_AA, threshold_orfs)

    return aa_conversion

    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
