"""
biom_read_Unifrac.py
BBIO 393 Computational Biology
Samuel L. Peoples

This script processes .biom file and creates output files and figures for use
in exploratory analysis. Boxplots, distributions, and pcoa plots are developed
from Jeff Gordon's A Core Gut Microbiome in Obese and Lean Twins for comparison
of dissimilarity between Lean-vs-Lean, Obese-vs-Obese, and Lean-vs-Obese samples.
"""

from biom import load_table
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib as mpl
import pandas as pd
import pylab as pl
import numpy as np
import os.path
import random
import csv
import os

def checks(filepath):
    """
    Ensures that the program will run.
    Checks filepaths for necessary files.
    """

    # Study directory
    if os.path.exists(filepath+"/study_77_011618-113533"):
        print(filepath+"/study_77_011618-113533 found.")
    else:
        print("Please ensure that "+filepath+"/study_77_011618-113533 is present.\n\t"
                +"define filepath=\"path-to-study\"\n\t"
                +"example: filepath = "+filepath)
        exit()

    # Figures directory
    if os.path.exists(filepath+"/figures"):
        print(filepath+"/figures found.")
    else:
        os.makedirs(filepath+"/figures")
        print(filepath+"/figures created.")

    # Stats directory
    if os.path.exists(filepath+"/stats"):
        print(filepath+"/stats found.")
    else:
        os.makedirs(filepath+"/stats")
        print(filepath+"/stats created.")

def single_rarefaction(filepath):
    """
    Runs single_rarefaction.py and returns output file location
    Sample size set to 1000
    """
    input = '/study_77_011618-113533/processed_data/219_otu_table.biom'
    output = '/study_77_011618-113533/processed_data/219_otu_table_even1000.biom'
    sample_size = '1000'

    # If the rarified table is present, there is no need to run it again.
    if os.path.exists(filepath+output):
        pass
    else:
        print("Rarefaction in progress. Calling:\n\t"
              +"single_rarefaction.py \n\t\t-i "+filepath+input
              +' \n\t\t-o '+filepath+output+' \n\t\t-d '+sample_size)
        os.system('single_rarefaction.py'+
                  ' -i '+filepath+input+
                  ' -o '+filepath+output+
                  ' -d '+sample_size)
    return output

def parse_table(filepath,rarefaction):
    """
    Passes the rarified table to be parsed
    Returns parsed table
    """
    # Load the table
    biom = load_table(filepath+rarefaction)

    # Define the observations and samples
    otus = biom.ids('observation')
    samples = biom.ids('sample')
    m = biom.matrix_data
    data = [pd.SparseSeries(m[i].toarray().ravel()) for i in np.arange(m.shape[0])]
    table = pd.SparseDataFrame(data, index=otus, columns = samples)
    counts(table)
    return table

def counts(table):
    """
    Counts the sum of the columns to verify that the rarefaction
    had been completed properly.
    """
    for sum in table.sum(axis=0):
        if sum != 1000:
            print("single_rarefaction.py failure.")
    print("Rarefaction check completed.")

def betaDiversity(filepath):
    """
    Runs beta_diversity.py with a weighted unifrac metric,
    and returns the beta diversity matrix as a DataFrame
    """
    input = '/study_77_011618-113533/processed_data/219_otu_table_even1000.biom'
    output_dir = '/stats'
    output = '/weighted_unifrac_219_otu_table_even1000.txt'
    metric = 'weighted_unifrac'
    tree = '/study_77_011618-113533/97_otus.tree'
     # If the dissimilarity matrix is present, There is no need to run it again.
    if os.path.exists(filepath+"/stats"+output):
        pass
    else:
        print("Dissimilarity Matrix preparation in progress. Calling:\n\t"
              +'beta_diversity.py \n\t\t-i '+filepath+input
              +' \n\t\t-o '+filepath+output_dir+' \n\t\t-m '+metric
              +' \n\t\t-t '+filepath+tree)
        os.system('beta_diversity.py'
              +' -i '+filepath+input
              +' -o '+filepath+output_dir
              +' -m '+metric
              +' -t '+filepath+tree)
    return pd.DataFrame.from_csv(filepath+output_dir+output, sep ='\t')

def label_tables(filepath, betas):
    """
    Returns label lists of sample IDs which 
    correspond to their values in the mapping file
    """
    ez_path = '/study_77_011618-113533/mapping_files/easy_mapping.csv'
    lean=[]
    obese=[]
    lines = []
    with open(filepath+ez_path,'r') as mapping:
        for line in mapping:
            lines.append(line.split(","))
        mapping.close()
    for line in lines:
        if str(line[2]).__contains__("Lean"):
            if line[0] in betas.keys():
                lean.append(line[0])
        elif str(line[2]).__contains__("Obese"):
            if line[0] in betas.keys():
                obese.append(line[0])
    return lean,obese

def break_table(filepath, betas, lean, obese):
    """
    Breaks the beta diversity matrix into Lean-vs-Lean, 
    Obese-vs-Obese, and Lean-vs-Obese. The function will
    not allow comparison of self (no distances of zero), 
    and will return lists of distances for each value.
    Each list is saved to its own csv file.
    """
    LL_stats = []
    OO_stats = []
    LO_stats = []

    # Separate distances to comparisons of
    # Lean-Lean, Obese-Obese, Lean-Obese
    for i in range(len(lean)):
        for j in range(len(betas[lean[i]].keys())):
            if betas[lean[i]].keys()[j] in lean:
                if betas[lean[i]][j] != 0:
                    LL_stats.append(betas[lean[i]][j])
            elif betas[lean[i]].keys()[j] in obese:
                LO_stats.append(betas[lean[i]][j])
    for i in range(len(obese)):
        for j in range(len(betas[obese[i]].keys())):
            if betas[obese[i]].keys()[j] in obese:
                if betas[obese[i]][j]!= 0:
                    OO_stats.append(betas[obese[i]][j])

    # Print the stats of the three categories
    print("Lean-vs-Lean:\n "+
          "Low: "+str(min(LL_stats))+
          "\n Mean: "+str(np.mean(LL_stats))+
          "\n Std: "+str(np.std(LL_stats))+
          "\n High: "+str(max(LL_stats))+
          "\n Count: "+str(len(LL_stats)))
    print("")
    print("Obese-vs-Obese:\n "+
          "Low: "+str(min(OO_stats))+
          "\n Mean: "+str(np.mean(OO_stats))+
          "\n Std: "+str(np.std(OO_stats))+
          "\n High: "+str(max(OO_stats))+
          "\n Count: "+str(len(OO_stats)))
    print("")
    print("Lean-vs-Obese:\n "+
          "Low: "+str(min(LO_stats))+
          "\n Mean: "+str(np.mean(LO_stats))+
          "\n Std: "+str(np.std(LO_stats))+
          "\n High: "+str(max(LO_stats))+
          "\n Count: "+str(len(LO_stats))+"\n")

    # Save the Unifrac distances to output csvs,
    print("Unifrac distances saved to: ")
    with open(filepath+"/stats/LL_stats_Unifrac.csv", "wb") as f:
        wr = csv.writer(f,quoting=csv.QUOTE_ALL)
        wr.writerow(LL_stats)
        f.close()
        print("\t Lean-vs-Lean: \n\t\t"+filepath+"/stats/LL_stats_Unifrac.csv")
    with open(filepath+"/stats/OO_stats_Unifrac.csv", "wb") as f:
        wr = csv.writer(f,quoting=csv.QUOTE_ALL)
        wr.writerow(OO_stats)
        f.close()
        print("\t Obese-vs-Obese: \n\t\t"+filepath+"/stats/OO_stats_Unifrac.csv")
    with open(filepath+"/stats/LO_stats_Unifrac.csv", "wb") as f:
        wr = csv.writer(f,quoting=csv.QUOTE_ALL)
        wr.writerow(LO_stats)
        f.close()
        print("\t Lean-vs-Obese: \n\t\t"+filepath+"/stats/LO_stats_Unifrac.csv")

    return LL_stats, OO_stats, LO_stats

def boxplots(filepath, LL_stats, OO_stats, LO_stats):
    """
    Creates three boxplots based on the LL, OO, and LO
    categories, and saves the boxplots to boxplot.png
    """
    mpl.use('agg')
    data = sample(LL_stats, OO_stats, LO_stats)
    fig = plt.figure(1, figsize=(9,6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data)
    ax.set_title('Comparison of Beta Diversity (Weighted Unifrac) Dissimilarity\n Sample of 1000')
    ax.set_xticklabels(['Lean vs Lean','Obese vs Obese', 'Lean vs Obese'])
    [flier.set(marker='o',color='#e7298a', alpha=.3) for flier in bp['fliers']]
    fig.savefig(filepath+"/figures/boxplot_unifrac.png", bbox_inches='tight')
    print("Boxplot saved to:\n\t "+filepath+"/figures/boxplot_unifrac.png")

def sample(LL_stats, OO_stats, LO_stats):
    """
    Returns a random sample of the three categories
    """
    return [random.sample(LL_stats, 1000),
            random.sample(OO_stats, 1000),
            random.sample(LO_stats, 1000)]

def distribution(filepath,LL_stats,OO_stats,LO_stats):
    """
    Visualize the Distributions of the
    Lean-vs-Lean, Obese-vs-Obese, and Lean-vs-Obese
    categories. Saves figures to output file
    """
    LL = sorted(LL_stats)
    OO = sorted(OO_stats)
    LO = sorted(LO_stats)
    LL_fit = stats.norm.pdf(LL,np.mean(LL),np.std(LL))
    OO_fit = stats.norm.pdf(OO,np.mean(OO),np.std(OO))
    LO_fit = stats.norm.pdf(LO,np.mean(LO),np.std(LO))

    # Clear any figures that may be present.
    pl.clf()

    print("Distributions saved to: ")
    # Plot the Lean vs Lean
    pl.plot(LL,LL_fit,'-o')
    pl.hist(LL,normed=True)
    pl.title("Weighted Unifrac Dissimilarity of Lean vs Lean Twins")
    pl.savefig(filepath+"/figures/LL_Distribution_Unifrac.png")
    pl.clf()
    print("\t Lean-vs-Lean: \n\t\t "+filepath+"/figures/LL_Distribution_Unifrac.png")

    # Plot the Obese vs Obese
    pl.plot(OO,OO_fit,'-o')
    pl.hist(OO,normed=True)
    pl.title("Weighted Unifrac Dissimilarity of Obese vs Obese Twins")
    pl.savefig(filepath+"/figures/OO_Distribution_Unifrac.png")
    pl.clf()
    print("\t Obese-vs-Obese: \n\t\t "+filepath+"/figures/OO_Distribution_Unifrac.png")
    #Plot the Lean vs Obese
    pl.plot(LO,LO_fit,'-o')
    pl.hist(LO,normed=True)
    pl.title("Weighted Unifrac Dissimilarity of Lean vs Obese Twins")
    pl.savefig(filepath+"/figures/LO_Distribution_Unifrac.png")
    pl.clf()
    print("\t Lean-vs-Obese: \n\t\t "+filepath+"/figures/LO_Distribution_Unifrac.png")

def pcoa(filepath):
    """
    Runs principal_coordinates.py and make_emperor.py
    to create an html file which allows the user to visualize
    the differences between the obesity categories
    """
    input = "/stats/weighted_unifrac_219_otu_table_even1000.txt"
    output = "/stats/weighted_unifrac_219_otu_table_even1000_pcoa.txt"

    # If the pcoa file is present, there is no need to run it again.
    if os.path.exists(filepath+output):
        pass
    else:
        print("PCoA in progress. Calling:\n\t"
              +"principal_coordinates.py \n\t\t-i "+filepath+input
              +' \n\t\t-o '+filepath+output)
        os.system('principal_coordinates.py'+
                  ' -i '+filepath+input+
                  ' -o '+filepath+output)
    print("Principal coordinates saved to: \n\t"+filepath+output)

    # If the html file is present, there is no need to run it again.
    input = output
    mapping = "/study_77_011618-113533/mapping_files/2485_mapping_file.txt"
    coloring = "obesitycat"
    output_dir = "/figures"
    output = "/figures/index.html"
    if os.path.exists(filepath+output):
        pass
    else:
        print("Emperor visualization in progress. Calling:\n\t"
              +"make_emperor.py \n\t\t-i "+filepath+input
              +' \n\t\t-o '+filepath+output)
        os.system('principal_coordinates.py'+
                  ' -i '+filepath+input+
                  ' -m '+filepath+mapping+
                  ' -b '+coloring+
                  ' -o '+filepath+output_dir)
    print("Principal coordinates saved to: \n\t"+filepath+output)

def main(filepath = "/home/qiime/Desktop/Project1"):
    """
    Define the path to the script, which should be in
    the same directory as study_77_011618-113533
    """

    checks(filepath)

    # Rarefaction of biom table, assigns path as variable
    rarefaction = single_rarefaction(filepath)

    # Parses the tables and labels
    table = parse_table(filepath,rarefaction)
    betas = betaDiversity(filepath)
    lean, obese = label_tables(filepath, betas)

    # Lean-vs-Lean, Obese-vs-Obese, and Lean-vs-Obese tables
    LL_stats, OO_stats, LO_stats = break_table(filepath,betas, lean, obese)

    # Create the boxplots
    boxplots(filepath, LL_stats,OO_stats,LO_stats)

    # Plot the Distributions
    distribution(filepath,LL_stats,OO_stats,LO_stats)

    # Plot the scatter
    pcoa(filepath)

if __name__ == '__main__':
    main()