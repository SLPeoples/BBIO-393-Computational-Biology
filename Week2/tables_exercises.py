import pandas as pd

"""
Simple matrix transformation
"""

X = pd.DataFrame([[0,1,0],
                  [1,0,0],
                  [0,0,1]])

y = pd.DataFrame([[1,0,0],
                  [0,0,1],
                  [0,1,0]])

Xy = X.dot(y)

print("X = \n"+str(X))
print("\ny = \n"+str(y))
print("\nX*y = \n"+str(Xy))
print()

"""
Let's say we have a string representing the DNA sequence.
"""

seq = "ATCGATCGATCGTAGCTGACTGATCTTCGGCACG"
print(seq)

seq_len = len(seq)
print("Sequence is of length: "+str(seq_len))

"""
Count nucleotide content
"""

a = 0
c = 0
t = 0
g = 0
for i in range(0,seq_len):
    if(seq[i] == "A"):
        a+=1
    elif(seq[i] == "C"):
        c+=1
    elif(seq[i] == "T"):
        t+=1
    elif(seq[i]=="G"):
        g+=1

print("Number of A: "+str(seq.count("A"))+", value from loop: "+str(a))
print("Number of T: "+str(seq.count("C"))+", value from loop: "+str(c))
print("Number of C: "+str(seq.count("T"))+", value from loop: "+str(t))
print("Number of G: "+str(seq.count("G"))+", value from loop: "+str(g))

GC_content = (g+c)/seq_len
print("The GC content is: "+str(GC_content))

"""
Two types of diversity include: Alpha(within sample), Beta(between samples)
"""