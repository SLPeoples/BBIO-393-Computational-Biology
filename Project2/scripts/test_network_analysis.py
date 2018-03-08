from network_analysis import parse_node_table
from network_analysis import parse_otu_node_table
from network_analysis import split_categories
from network_analysis import parse_stats
from network_analysis import individual_stats
from unittest import TestCase, main
import pandas as pd
import os

__author__ = "Samuel L. Peoples"
__credits__ = ["Dr. Jesse Zaneveld"]
__email__ = "contact@lukepeoples.com"
__status__ = "Testing"


class NetworkAnalysisTests(TestCase):
    def setUp(self):
        """
        Sets up filepaths and variables that the program will need for various tests.
        """
        self.node_file = "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_node_table.txt"
        self.edge_file = "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_edge_table.txt"
        self.output_file = "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/results"
        self.feature = "feature"
        self.categories = ["cat_zero", "cat_one"]
        self.n_iterations = 1000
        self.verbose = False

        self.df_union = pd.DataFrame({"from":["a","i","b","j","c","d","e","f","g","h"],
                                      "to":[1,1,2,2,3,4,5,6,7,8],
                                      "feature":["cat_zero","cat_one","cat_zero","cat_one","cat_zero","cat_zero",
                                                 "cat_zero","cat_one","cat_one","cat_one"],
                                      "degree":[2,2,2,2,1,1,1,1,1,1,]})
        self.cat_0_table = self.df_union[self.df_union["feature"]=="cat_zero"]
        self.cat_1_table = self.df_union[self.df_union["feature"]=="cat_one"]
        self.otu_0_table = pd.DataFrame.from_csv(
            "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_cat_0_list.txt", sep='\t')
        self.otu_1_table = pd.DataFrame.from_csv(
            "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_cat_1_list.txt", sep='\t')
        self.otu_both_table = pd.DataFrame.from_csv(
            "C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_cat_b_list.txt", sep='\t')


    def test_parse_node_table_correct(self):
        """
        Testing that a test node file returns two properly separated dataframes
        """
        cat_0_output, cat_1_output = parse_node_table(self.node_file,self.feature,self.categories,self.verbose)
        assert cat_0_output["feature"].all() == "cat_zero"
        assert cat_1_output["feature"].all() == "cat_one"

    def test_parse_node_table_bad_path(self):
        """
        Ensures the program will not run without proper filepaths
        """
        with self.assertRaises(FileNotFoundError):
            parse_node_table("bad path", self.feature, self.categories, self.verbose)

    def test_parse_node_table_bad_feature(self):
        """
        Ensures the program will not run without proper feature column definitions
        """
        with self.assertRaises(KeyError):
            parse_node_table(self.node_file, "bad feature", self.categories, self.verbose)
    
    def test_parse_node_tabe_bad_categories(self):
        """
        Ensures the program with not run without proper categories
        """
        cat_0_output, cat_1_output = parse_node_table(self.node_file, self.feature, ["bad","categories"], self.verbose)
        assert len(cat_0_output) == 0
        assert len(cat_1_output) == 0
    
    def test_parse_otu_node_table_correct(self):
        """
        Ensures the union of the edge and node file are joined as expected
        """
        df_union = parse_otu_node_table(self.node_file, self.edge_file, self.feature, self.verbose)
        assert (self.df_union["from"] == df_union["from"]).all() == True
        assert (self.df_union["to"] == df_union["to"]).all() == True
        assert (self.df_union["degree"] == df_union["degree"]).all() == True
        assert (self.df_union["feature"] == df_union["feature"]).all() == True

    def test_parse_otu_node_table_bad_path_node(self):
        """
        Ensures the program will not run without a proper filepath
        """
        with self.assertRaises(FileNotFoundError):
            parse_otu_node_table("bad path", self.edge_file, self.feature, self.verbose)

    def test_parse_otu_node_table_bad_path_edge(self):
        """
        Ensures the program will not run without a proper filepath
        """
        with self.assertRaises(FileNotFoundError):
            parse_otu_node_table(self.node_file, "bad path", self.feature, self.verbose)

    def test_parse_otu_node_table_bad_feature(self):
        """
        Ensures the program will not run without proper feature column definitions
        """
        with self.assertRaises(KeyError):
            parse_otu_node_table(self.node_file, self.edge_file, "bad feature", self.verbose)
    
    def test_split_categories_correct(self):
        """
        Ensures the program separates the dataframes as expected
        """
        df_union = parse_otu_node_table(self.node_file, self.edge_file, self.feature, self.verbose)
        otu_0_table, otu_1_table, otu_both_table = split_categories(df_union, self.categories, self.feature, self.verbose)
        assert len(otu_0_table) == 3
        assert len(otu_1_table) == 3
        assert len(otu_both_table) == 2
    
    def test_individual_stats_correct(self):
        """
        Ensures the monte carlo, sampling, and statistics are calculated as expected.
        """
        cat_0_stats = individual_stats(self.cat_0_table, self.n_iterations, self.verbose, "").split("\t")
        cat_1_stats = individual_stats(self.cat_1_table, self.n_iterations, self.verbose, "").split("\t")
        stats_otu_0 = individual_stats(self.otu_0_table, self.n_iterations, self.verbose, "").split("\t")
        stats_otu_1 = individual_stats(self.otu_1_table, self.n_iterations, self.verbose, "").split("\t")
        stats_otu_b = individual_stats(self.otu_both_table, self.n_iterations, self.verbose, "").split("\t")

        assert cat_0_stats[1] == " Min: 1.0"
        assert cat_0_stats[6] == " Max: 2.0"

        assert cat_1_stats[1] == " Min: 1.0"
        assert cat_1_stats[6] == " Max: 2.0"

        assert stats_otu_0[1] == " Min: 1.0"
        assert stats_otu_0[6] == " Max: 1.0"

        assert stats_otu_1[1] == " Min: 1.0"
        assert stats_otu_1[6] == " Max: 1.0"

        assert stats_otu_b[1] == " Min: 2.0"
        assert stats_otu_b[6] == " Max: 2.0"

    def test_parse_stats_correct(self):
        """
        Ensures the program saves the output file.
        """
        df_union = parse_otu_node_table(self.node_file, self.edge_file, self.feature, self.verbose)
        otu_0_table, otu_1_table, otu_both_table = split_categories(df_union, self.categories, self.feature,
                                                                    self.verbose)
        parse_stats(self.feature, self.categories, self.cat_0_table, self.cat_1_table, otu_0_table, otu_1_table, otu_both_table, self.n_iterations,
         self.output_file, self.verbose)
        assert os.path.isfile(self.output_file+"/"+str(self.feature)+"_network_analysis.txt")

if __name__ == "__main__":
    main()