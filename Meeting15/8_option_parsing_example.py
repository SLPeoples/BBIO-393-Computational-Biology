#!/usr/bin/env python
from __future__ import division

__author__ = "AUTHOR_NAME"
__copyright__ = "COPYRIGHT_INFORMATION"
__credits__ = ["AUTHOR_NAME"]
__license__ = "GPL"
__version__ = "1.6.0dev"
__maintainer__ = "AUTHOR_NAME"
__email__ = "AUTHOR_EMAIL"
__status__ = "Development"


from argparse import ArgumentParser, RawDescriptionHelpFormatter,FileType
#Documentation can be found here:https://docs.python.org/2/library/argparse.html#module-argparse

def make_commandline_interface():
    """Returns a parser for the commandline"""
    short_description =\
    """
    This is a template script for how to use python's argparse module.
    """

    long_description=\
    """
    This is a template script demonstrating how to use pythons argparse module.
    When actually adapting the script, you would fill in your own script
    description here.
    
    Rationale
    ---------

    You can include a rationale for the overall approach of your script in the script
    description

    References
    ----------
    Stick references you used in developing your script here.
    """

    parser = ArgumentParser(description=short_description,\
      epilog=long_description,formatter_class = RawDescriptionHelpFormatter)
   
    #Required parameters 
    parser.add_argument('-i','--input_file',type=FileType("U"),required=True,\
      help='path to an input FASTA file')


    #Optional parameters
    #NOTE: these should have sensible default values specified with 
    # default = 'whatever'

    #Example of output to a default location
    parser.add_argument('-o','--output_file',type=FileType("w+"),default = 'results.txt',
      help='path to output data. Default: %(default)s')

    #Example of defining an argument that only allows specific choices
    parser.add_argument('-m','--method',default='unweighted',\
      choices=['weighted','unweighted'],\
      help="select a method. Default:%(default)s")

    #Example of taking in an integer value (only)
    parser.add_argument('-n','--n_permutations',type=int,default=1000,\
      help="select a number of Monte Carlo permutations. Default:%(default)s")
    
    #Example of a 'flag option' that sets a variable to true if provided 
    parser.add_argument('-v','--verbose',default=False,action='store_true',\
      help="display verbose output while program runs")

    #Add version information (from the __version__ string defined at top of script
    parser.add_argument('--version',action='version',version=__version__,\
      help="display version number and exit")

    return parser

def main():
    """Main function"""
    parser = make_commandline_interface()
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    method = args.method
    verbose = args.verbose
    
    if verbose:
        print("Input file:",input_file)
        print("Output file:",output_file)
        print("Method:",method)
    

    

if __name__ == "__main__":
    main()

