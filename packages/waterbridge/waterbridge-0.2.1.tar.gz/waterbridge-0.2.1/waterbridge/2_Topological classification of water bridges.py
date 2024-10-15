###########################################################################################################################
#                                      Topological classification of water bridges                                        #
###########################################################################################################################
# Importing the required modules.
import os

# List of nucleotides and amino acids.
NT = ['-  A', '-  U', '-  G', '-  C']
AA = ['-GLY', '-ALA', '-SER', '-THR', '-CYS', '-VAL', '-LEU', '-ILE', '-MET', '-PRO', '-PHE', '-TYR', '-TRP', '-ASP', '-GLU', '-ASN', '-GLN', '-HIS', '-LYS', '-ARG']


# User-defined function to extract PDB record and identity of interacting amino acids and nucleotides. 
# List 'aanb_info' contains PDB record (chain number, residue number) of interacting amino acids and 
# nucleotides. For example: 'Q0030-THR'. 
# List 'aa_nt' contains the identity of interacting amino acids and nucleotides. For example: 'THR'. 
def aa_nt_name(splitted_list_name):
    for i in range(len(splitted_list_name)):
        if i+1 < len(splitted_list_name):
            if splitted_list_name[i+1][:10] not in aanb_info:
                aanb_info.append(splitted_list_name[i+1][:10])
                                                                
    for j in aanb_info:                                                    
        aa_nt.append(j[6:])

# Read any of the three output files of previously identified water bridges.
file_waterbridges = 'waterbridges.txt'
file = open(file_waterbridges, 'r')
i = -1
start_line_plus_first_line = []
end_line = []
my_dict = {"pdb":[],"val":[]}
pdb = []
data = file.readlines()
for lines in data: 
    i += 1
    if lines.find('.hb2') >= 0:
        start_line_plus_first_line.append(i)
    elif lines.find('.....................................') >= 0:
        end_line.append(i)

for n in range(len(start_line_plus_first_line)):
    for m in range(len(end_line)):
        if n == m:
            my_dict["pdb"].append(data[start_line_plus_first_line[n]])
            my_dict["val"].append(data[start_line_plus_first_line[n]+1:end_line[m]])

for l in range(len(my_dict['val'])):
    for nm in my_dict['val'][l]:
        # List contains PDB record (chain number, residue number) of interacting amino acids and
        # nucleotides. For example - Q0030-THR. 
        aanb_info = []
        # List 'aa_nt' contains identity of interacting amino acids and nucleotides. For example: 'THR'. 
        aa_nt = []
        x1 = nm.split('[')[0]  # x1 contains the upper topology only
        x2 = x1.split('---') # x2 is direct hydrogen bonds b/w amino acid and nucleotide.
        aa_nt_name(x2) # Extracting PDB record and identity of interacting amino acids and nucleotides.
        
        # Counting the number of amino acids and nucleotides involved in water bridge formation.
        aa =  len([i for i in aa_nt if i in AA ])
        nt =  len([i for i in aa_nt if i in NT ])
        
        # Saving water bridges as per their topology.
        filename = 'A' + str(aa) + '-w-N' + str(nt) + '.txt' 
        path = os.getcwd()
        directory = os.listdir(path)  # specify folder path.
        if filename in directory: 
            out_files = open(filename, 'r')
            if my_dict['pdb'][l] not in out_files: 
                print(my_dict['pdb'][l], file=open(filename, "a"))
        else:
            print(my_dict['pdb'][l], file=open(filename, "a"))
        print(nm, file=open(filename, "a"))
        
        
