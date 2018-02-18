"""
Read a tab-delimited table
"""
from sys import argv

def main():
    #Open a file, skip the headers, and parse lines
    infile = argv[1]
    f = open(infile)
    header = None
    for i,line in enumerate(f.readlines()):
             
        fields = line.strip('\n').split("\t")

        if i == 0:
            header = fields
            header_map = {}
            for j,field in enumerate(header):
                header_map[field] = j
        
        desired_column = 'Size_cm'
        column_index = header_map[desired_column]         
        column_value = fields[column_index]
        print(column_value)

if __name__ == "__main__":
    main()
