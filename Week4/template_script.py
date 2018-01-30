from random import choice, shuffle
from sys import argv 

"""
This script returns sequence lengths from a
file of sequences.
"""

__version__ = 1.0
__authors__ = ["Jesse Zaneveld"]
__copyright__ = "CC0"

def seq_length(seq,remove_gaps=True):
   """Return the length of a DNA sequence
    
    seq -- a string of DNA nucleotides like 'ACTGGTA'

    remove_gaps -- if True, remove gaps like '-' 
      before calculating sequence length    
   """
   result = len(seq) 
   return result

def sequence_lengths_from_file(lines):
    """Return sequence lengths from lines
    lines -- lines of a FASTA file
    """
    sequence_lengths = []
    for line in lines:
        line = line.strip()
        line_length = seq_length(line)
        sequence_lengths.append(line_length)
    
    return sequence_lengths

def main():
    print("User arguments:",argv)

    if len(argv) < 2:
        print("Usage: python template_script.py input_fasta.txt")
        exit()

    #We know the user has passed in arguments!
    input_file = argv[1]
    fasta_file = open(input_file,"U")
    sequence_lengths = sequence_lengths_from_file(fasta_file)
    print(sequence_lengths)

    import matplotlib.pyplot as plt
    x = sequence_lengths
    plt.plot(x)
    plt.ylabel('nucleotide lengths')
    plt.xlabel('seq #')
    plt.show()

if __name__ == "__main__":
    main()

