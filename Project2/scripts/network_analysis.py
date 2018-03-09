#!/usr/bin/env python
from __future__ import division
import pandas as pd
import os

__author__ = "Samuel L. Peoples"
__credits__ = ["Dr. Jesse Zaneveld"]
__version__ = "0.0.1"
__email__ = "contact@lukepeoples.com"
__status__ = "Development"

from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
# Documentation can be found here:https://docs.python.org/2/library/argparse.html#module-argparse

def make_commandline_interface():
    """Returns a parser for the commandline"""
    short_description = \
        """
        network_analysis.py; analyze statistics of degree comparing between two categories of feature column.
        Example: \t network_analysis.py  \n\t\t
            -node {PATH to NODE FILE} \n\t\t
            -edge {PATH to EDGE FILE} \n\t\t
            [-o {PATH to OUTPUT DIRECTORY}] \n\t\t
            -f {FEATURE COLUMN for comparison} \n\t\t
            -c {CATEEGORY of FEATURE} {CATEGORY of FEATURE}\n\t\t
            [-n {N_ITERATIONS for Monte Carlo Simulation}]
        """

    long_description = \
        """
        This script will analyze statistics between two categories of a feature column in a node table.
        Returns output text file with statistics for the degree of each category, and otus associated with the 
        respective categories, as well as both. Accuracy of the statistics can be controlled with n_iterations.
    
        Rationale
        ---------
    
        Comparing the degree of the different categories of a feature column can display a disparity of otu frequency 
        in one category, or the other. This translates to a statistically significant difference between the microbial 
        communities with respect to the categories analyzed.
    
        References
        ----------
        Qiime: http://qiime.org/
        Qiita: https://qiita.ucsd.edu/
        Gut Microbiome Dataset: https://qiita.ucsd.edu/study/description/77
        Biom-Format: http://biom-format.org/documentation/biom_format.html
        Cytoscape: http://www.cytoscape.org/documentation_users.html
        Make_otu_network.py: http://qiime.org/scripts/make_otu_network.html 
        
        Notes
        ----------
        Given a BIOM and Mapping File, the following example can be used to generate the necessary node and edge files.
        Requires QIIME.
        
        Rarify the table for increased accuracy
            single_rarefaction.py -i 'sample.biom' -o 'sample_1000.biom' -d 1000
        
        Filter any samples that you are not analyzing. Here, we do not want 'Overweight' samples.
            filter_samples_from_otu_table.py 
                -i 'sample_1000.biom' -m 'mapping_file.txt' -o 'sample1000_filtered.biom' 
                --output_mapping_fp 'mapping_file_filtered.txt' -s 'obesitycat:*,!Overweight' 
        
        Make the otu network with the filtered biom and mapping file, here we wanted properties based on "obesitycat"
            make_otu_network.py 
                -i 'sample_1000_filtered.biom' -m mapping_file_filtered.txt -o otu_network_filtered  -b "obesitycat"
        """

    parser = ArgumentParser(description=short_description, \
                            epilog=long_description, formatter_class=RawDescriptionHelpFormatter)

    # Required parameters
    parser.add_argument('-node', '--node_file', type=str, required=True, \
                        help='PATH to an input NODE FILE, output from make_otu_network.py')

    parser.add_argument('-edge', '--edge_file', type=str, required=True, \
                        help='PATH to an input EDGE FILE, output from make_otu_network.py')

    parser.add_argument('-f', '--feature', type=str, required=True, \
                        help='Name of the FEATURE column for analysis')

    parser.add_argument('-c', '--categories', type=str, nargs=2, required=True, \
                        help='Name of CATEGORIES within the feature column for analysis, two (2) required.')
    # Optional parameters
    parser.add_argument('-o', '--output_file', type=str, default='',
                        help='PATH to output DIRECTORY. Default: .~\[feature]_network_analysis.txt')

    parser.add_argument('-n', '--n_iterations', type=int, default=1000, \
                        help="Number of iterations for the analysis, will take samples for n iterations. Default:%(default)s")

    # Example of a 'flag option' that sets a variable to true if provided
    parser.add_argument('-v', '--verbose', default=True, action='store_true', \
                        help="display verbose output while program runs. Default:%(default)s")

    # Add version information (from the __version__ string defined at top of script
    parser.add_argument('--version', action='version', version=__version__, \
                        help="display version number and exit")

    return parser


def parse_node_table(node_file, feature, categories, verbose):
    """
    Parses the node table's user_nodes degree and feature,
    returns separated DataFrames based on feature categories.
    :param node_file: filepath to node file
    :param feature: feature column for analysis
    :param categories: categories of feature column
    :param verbose: verbosity
    :return: DataFrame for each category containing node_disp_name, degree, and feature
    """
    if verbose:
        print("Parsing "+str(node_file))

    # Read the node file
    df = pd.read_csv(node_file, sep="\t")
    # Save just user nodes
    df = df[df.ntype == "user_node"]
    # Reduce the node file DataFrame
    df = df[["node_disp_name", "degree", feature]]
    # Separate the DataFrame into the two defined categories
    cat_0_table = df[df[feature] == categories[0]]
    cat_1_table = df[df[feature] == categories[1]]
    # Return the tables
    return cat_0_table, cat_1_table


def parse_otu_node_table(node_file, edge_file, feature,verbose):
    """
    Parses the otu nodes by joining the data in the edge file with the node file. Returns DataFrame for OTUs in each
    category respectively, and both categories.
    :param node_file: filepath to node file
    :param edge_file: filepath to edge file
    :param feature: feature column for analysis
    :param categories: categories of the feature column
    :param verbose: verbosity
    :return: DataFrame containing from, to, degree, and feature for each category respectively and both categories.
    """
    if verbose:
        print("Parsing "+str(edge_file))
    # Read the node file
    node_column_list = ["node_name", "degree", feature]
    df_node = pd.read_csv(node_file, sep="\t")
    df_node = df_node[df_node.node_name != "NaN"]
    df_node = df_node[node_column_list]

    # Read the edge file
    edge_column_list = ["from", "to", feature]
    df_edge = pd.read_csv(edge_file, sep="\t")
    df_edge = df_edge[edge_column_list]

    # Wrangling to join the degree, from, to and feature columns
    df_edge.rename(columns={'to': 'to'}, inplace=True)
    df_edge = df_edge.sort_values(by=['to'])
    df_edge['to'] = df_edge['to'].convert_objects(convert_numeric=True) # Doesn't work with to_numeric
    df_node.rename(columns = {'node_name':'to'},inplace=True)
    df_node = df_node.sort_values(by=['to'])
    df_node['to'] = df_node['to'].convert_objects(convert_numeric=True) # Doesn't work with to_numeric

    # Join the tables
    df_union = df_edge.merge(df_node,how='inner', on='to')
    df_union = df_union.drop([str(feature)+"_y"],axis=1)
    df_union.rename(columns = {(feature+'_x'):str(feature)},inplace=True)

    if verbose:
        print("\nUnioned DataFrame: ")
        print(df_union.head(n=10))
        print("\t ...")
    return df_union


def split_categories(df_union, categories, feature, verbose):
    """
    Splits the unioned DF into three DFs with unique OTU nodes; cat_0 only, cat_1, only, cat_both
    :param df_union: Joined dataframe
    :param categories: categories of feature
    :param feature: Feature column for testing
    :param verbose: verbostiy
    :return: cat_0_table, cat_1_table, cat_both_table
    """
    # List of otu node identifiers for comparison
    to_list = []
    cat_0_list = []
    cat_1_list = []

    # Create feature lists
    for row in df_union.iterrows():
        if row[1][2] == categories[0]:
            cat_0_list.append(row[1][1])
        elif row[1][2] == categories[1]:
            cat_1_list.append(row[1][1])

    # Strip the lists into cat_0 only, cat_1 only, and both
    set_b = set(cat_0_list) & set(cat_1_list)
    for cat_0 in cat_0_list:
        if cat_0 in set_b:
            to_list.append(cat_0)
    for cat_1 in cat_1_list:
        if cat_1 in set_b:
            if cat_1 not in to_list:
                to_list.append(cat_1)
    for item in to_list:
        if item in cat_0_list:
            cat_0_list.remove(item)
        elif item in cat_1_list:
            cat_1_list.remove(item)

    # Lists for the first category's DataFrame
    from_0 = []
    to_0 = []
    deg_0 = []
    feat_0 = []

    # Lists for the second category's DataFrame
    from_1 = []
    to_1 = []
    deg_1 = []
    feat_1 = []

    # Lists for the otus which appear in both categories
    from_b = []
    to_b = []
    deg_b = []
    feat_b = []

    u_to_list = []
    u_0_list = []
    u_1_list = []

    # Populate separated DataFrames, reduce tables to distinct OTU nodes;
    # Couldn't break into a separate function
    for row in df_union.iterrows():
        if row[1][1] in to_list:
            if row[1][1] not in u_to_list:
                u_to_list.append(row[1][1])
                from_b.append(row[1]['from'])
                to_b.append(row[1]['to'])
                deg_b.append(row[1][feature])
                feat_b.append(row[1]['degree'])
        elif row[1][1] in cat_0_list:
            if row[1][1] not in u_0_list:
                u_0_list.append(row[1][1])
                from_0.append(row[1]['from'])
                to_0.append(row[1]['to'])
                deg_0.append(row[1][feature])
                feat_0.append(row[1]['degree'])
        elif row[1][1] in cat_1_list:
            if row[1][1] not in u_1_list:
                u_1_list.append(row[1][1])
                from_1.append(row[1]['from'])
                to_1.append(row[1]['to'])
                deg_1.append(row[1][feature])
                feat_1.append(row[1]['degree'])

    # Create the first category's DataFrame
    cat_0_final = {"from": from_0, "to": to_0, feature: feat_0, "degree": deg_0}
    otu_0_table = pd.DataFrame(data=cat_0_final)
    otu_0_table.rename(columns={feature: 'degree', 'degree': feature}, inplace=True)

    # Create the second category's DataFrame
    cat_1_final = {"from": from_1, "to": to_1, feature: feat_1, "degree": deg_1}
    otu_1_table = pd.DataFrame(data=cat_1_final)
    otu_1_table.rename(columns={feature: 'degree', 'degree': feature}, inplace=True)

    # Create the DataFrame for otus which appear in both categories
    cat_both_final = {"from": from_b, "to": to_b, feature: feat_b, "degree": deg_b}
    otu_both_table = pd.DataFrame(data=cat_both_final)
    otu_both_table.rename(columns={feature: 'degree', 'degree': feature}, inplace=True)

    if verbose:
        print(categories[0] + " Only:")
        print(otu_0_table.head(n=10))
        print("\t\t ...")
        print(categories[1] + " Only:")
        print(otu_1_table.head(n=10))
        print("\t\t\t ...")
        print("Both " + categories[0] + " and " + categories[1] + ":")
        print(otu_both_table.head(n=10))
        print("\t\t\t\t ...")
    return otu_0_table, otu_1_table, otu_both_table


def parse_stats(feature, categories, cat_0_table, cat_1_table, otu_0_table, otu_1_table, otu_both_table, n_iterations, output_file, verbose):
    """
    Parse the statistics for each DataFrame by averaging n_iterations of random samples. Finds Min, Q1, Mean,
    Median, Q3, Max, and Standard Deviation over the iterations.
    :param feature: feature column for analysis
    :param categories: categories of the feature column
    :param cat_0_table: user_node degree DataFrame for the first category
    :param cat_1_table: user_node degree DataFrame for the second category
    :param otu_0_table: otu_node degree DataFrame which is associated with the first category only.
    :param otu_1_table: otu_node degree DataFrame which is associated with the second category only.
    :param otu_both_table: otu_node degree DataFrame which is associated with both categories.
    :param n_iterations: number of iterations for the analysis
    :param output_file: output file location, appends with the feature category and network_analysis.txt
        ex: C:/.../data/output/feature_network_analysis.txt
    :param verbose: verbosity
    """
    v_string = "Processing statistics for "+categories[0]+" nodes, for "+str(n_iterations)+" iterations, with samples of 40."
    # Parse the stats for the first category
    stats_0 = individual_stats(cat_0_table, n_iterations, verbose, v_string)

    v_string = "Processing statistics for "+categories[1]+" nodes, for "+str(n_iterations)+" iterations, with samples of 40."
    # Parse the stats for the second category
    stats_1 = individual_stats(cat_1_table, n_iterations, verbose, v_string)

    v_string = "Processing statistics for otu nodes connected to " + categories[0] + " only, for " + str(
        n_iterations) + " iterations, with samples of 40."
    # Parse the stats for the otus associated with the first category only
    stats_otu_0 = individual_stats(otu_0_table, n_iterations, verbose, v_string)

    v_string = "Processing statistics for otu nodes connected to " + categories[1] + " only, for " + str(
            n_iterations) + " iterations, with samples of 40."
    # Parse the stats for the otus associated with the second category only
    stats_otu_1 = individual_stats(otu_1_table, n_iterations, verbose, v_string)

    v_string = "Processing statistics for otu nodes connected to both " + categories[0] + " and " + categories[
            1] + ", for " + str(n_iterations) + " iterations, with samples of 40."
    # Parse the stats for the otus associated with both categories
    stats_otu_b = individual_stats(otu_both_table, n_iterations, verbose, v_string)

    # Save the stats to the output file location
    outfile = open(output_file+"/"+str(feature)+"_network_analysis.txt",'w')
    outfile.write(categories[0] + ":\n" + stats_0+"\n")
    outfile.write(categories[1] + ":\n" + stats_1+"\n")
    outfile.write(categories[0] + "Only :\n" + stats_otu_0+"\n")
    outfile.write(categories[1] + "Only :\n" + stats_otu_1+"\n")
    outfile.write("Both " + categories[0] + " and " + categories[1] + ":\n" + stats_otu_b+"\n")
    outfile.close()

    #Print the stats
    if verbose:
        print("Statistics:")
        print(categories[0] + ":\n" + stats_0)
        print(categories[1] + ":\n" + stats_1)
        print(categories[0] + "Only :\n" + stats_otu_0)
        print(categories[1] + "Only :\n" + stats_otu_1)
        print("Both "+ categories[0] + " and " + categories[1] + ":\n" + stats_otu_b)
        print("Output saved to: "+output_file+"/"+str(feature)+"_network_analysis.txt")


def individual_stats(table, n_iterations, verbose, v_string):
    """
    Individual stats for each table passed in
    :param table: DataFrame with column labeled 'degree'
    :param n_iterations: number of iterations for the test
    :return: string containing statistics; Min, Q1, Mean, Median, Q3, Max, Std_Dev
    """
    if verbose:
        print(v_string)

    # Define lists for the stats
    minimum = []
    q1 = []
    mean_val = []
    median_val = []
    q3 = []
    maximum = []
    std_dev = []

    # Save the original table for sampling
    orig = table
    for i in range(n_iterations):
        # Take a sample
        table = orig.sample(n=40,replace=True)
        # Append the lists
        minimum.append(table.degree.min())
        q1.append(table.degree.quantile(.25))
        mean_val.append(table.degree.mean())
        median_val.append(table.degree.quantile(.5))
        q3.append(table.degree.quantile(.75))
        maximum.append(table.degree.max())
        std_dev.append(table.degree.std())

    # Create a DataFrame of Stats
    d = {'minimum': minimum, 'q1': q1, 'mean_val': mean_val, 'median_val': median_val, 'q3': q3, 'maximum': maximum,
           'std_dev': std_dev}
    df = pd.DataFrame(data=d)

    # Build the stats string to return
    stats = ("\t Min: " + str(round(df.minimum.mean(), 3))
          + "\t 1Q: " + str(round(df.q1.mean(), 3))
          + "\t Mean: " + str(round(df.mean_val.mean(), 3))
          + "\t Median: " + str(round(df.median_val.mean(), 3))
          + "\t 3Q: " + str(round(df.q3.mean(), 3))
          + "\t Max: " + str(round(df.maximum.mean(), 3))
          + "\t Std: " + str(round(df.std_dev.mean(), 3)))
    return stats


def main():
    """Main function"""
    parser = make_commandline_interface()
    args = parser.parse_args()

    node_file = args.node_file
    if not os.path.isfile(node_file):
        print(node_file+" not found. Please verify location.")
        exit(0)
    edge_file = args.edge_file
    if not os.path.isfile(edge_file):
        print(edge_file+" not found. Please verify location.")
        exit(0)
    output_file = args.output_file
    if not os.path.isdir(output_file):
        print(node_file+" not found. Please verify location.")
        exit(0)

    feature = args.feature
    categories = args.categories
    n_iterations = args.n_iterations
    verbose = args.verbose

    if verbose:
        print("network_analysis.py")
        print("\t Node file:", node_file)
        print("\t Edge file:", edge_file)
        print("\t Output filepath:", output_file)
        print("\t Feature: ", feature)
        print("\t Categories: ", categories)
        print("\t n_iterations: ", n_iterations)

    cat_0_table, cat_1_table = parse_node_table(node_file, feature, categories, verbose)
    df_union = parse_otu_node_table(node_file, edge_file, feature, verbose)
    otu_0_table, otu_1_table, otu_both_table = split_categories(df_union, categories, feature, verbose)

    parse_stats(feature, categories, cat_0_table, cat_1_table, otu_0_table,
                otu_1_table, otu_both_table, n_iterations, output_file, verbose)


if __name__ == "__main__":
    main()