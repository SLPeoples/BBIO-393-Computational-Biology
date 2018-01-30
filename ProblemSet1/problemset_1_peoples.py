from random import choice, shuffle

# Samuel L. Peoples
# PS1
def problem0(seq):
    """Calculate the length of a seq
    seq -- a string of DNA nucleotides like 'ACTGGTA'
    You don't need to do anything for this problem.
    It is an example of how to format your results.
    The info you get is up above in the parameters
    for the function. Do your calculations, and 
    save them to a 'result' variable, then use
    return result.
    """
    result = len(seq)
    return result


def problem1(seq):
    """Calculate the GC content of a DNA sequence
    seq -- a string of A,T,C, or G DNA nucleotides
    Extra challenge: if this is too easy, update your
    code to handle N (ambiguous) characters. 
    """
    g = seq.lower().count("g")
    c = seq.lower().count("c")
    a = seq.lower().count("a")
    t = seq.lower().count("t")
    return (g + c) / (g + c + a + t)


def problem2(gene_names):
    """Select the last gene from a list of gene names
    gene_names -- a list of gene names
    """
    return gene_names[-1]


def problem3(tumor_loads):
    """Return tumor load squared for each tumor load in a list
    tumor_loads -- a list of tumor loads expressed 
      as floating point numbers 
      (example: [0.0,3.0,15.0,100.0]
    """
    return [(x * x) for x in tumor_loads]


def problem4(gene_list, gene_functions):
    """Return a list of gene function for each gene id
     gene_list -- a list of gene ids (each gene id is a
     string)
     gene_functions -- a dict of functions for each gene
     the keys will be the id of each gene, the values
     will be the function of that gene
    """
    return [gene_functions[gene] for gene in gene_list]


def problem5(fasta_lines):
    """Write each fasta line to a 'results.txt' file in 
    fasta format."""

    # Hint: file operations are described at length in
    # Chapter 3.

    fasta = open("results.txt", "w")
    [fasta.write(line) for line in fasta_lines]
    fasta.close()


def main():
    """This function will hold your answers to all problems"""

    # Problem 0. This is an example problem to
    # show what I want.
    problem0_seq = "ATGCTAGCTAGCTGCG\n"
    p0_answer = problem0(problem0_seq)
    print("Problem 0 solution:", p0_answer)

    # Problem 1.
    problem1_seq = "GGGCTAGCAGGGGTCAGTCGTGCGTACGTAGCTCGATCGTACGCTAGCTCAGCTCAGGCGGGGGGCGCATGCTCAGACTAGCTACGTACGTACGCGCTGACGTCGATCGACTGCGCGTCTAC"
    p1_answer = problem1(problem1_seq)
    print("Problem 1 solution:", p1_answer)

    # Problem 2.
    gene_names = ['cdhA', 'cdhB', 'chdC', 'tmuM']
    p2_answer = problem2(gene_names)
    print("Problem 2 solution:", p2_answer)

    # Problem 3.
    tumor_loads = [17.0, 0.0, 0.0, 15.0, 17.0, 45.0, 253.0]
    p3_answer = problem3(tumor_loads)
    print("Problem 3 solution:", p3_answer)

    # Problem 4.
    microarray_gene_ids = ["1494_f_at", "1431_at", "131_at"]
    gene_functions = {"1005_at": "dual specificity phosphatase 1(DUSP1)",
                      "1494_f_at": "cytochrome P450 family 2 subfamily A member 6(CYP2A6)",
                      "1431_at": "cytochrome P450 family 2 subfamily E member 1(CYP2E1)",
                      "1263_at": "interleukin 3(IL3)", "131_at": "TATA-box binding protein associated factor 11(TAF11)"}
    p4_answer = problem4(microarray_gene_ids, \
                         gene_functions)
    print("Problem 4 solution:", p4_answer)

    # Problem 5.
    fasta_lines = [">gene1\n", "ACTGAGTAGTTGA\n", ">gene2\n", "ATCGATCGTACGATTCGTACGACTG\n", ">gene3\n",
                   "ACTTATTCATAC\n"]
    p5_answer = problem5(fasta_lines)
    print("Problem 5 solution:", p5_answer)


if __name__ == "__main__":
    main()
