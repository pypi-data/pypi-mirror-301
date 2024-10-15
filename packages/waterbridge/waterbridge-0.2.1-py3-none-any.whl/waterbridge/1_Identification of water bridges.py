###########################################################################################################################
#                                        Identification of water bridges                                                  #
###########################################################################################################################
# Importing the required modules
import os, re, itertools

# A used defined function to remove ambiguity arising due to hydrogen bond donor as well as acceptor nature of 
# some atoms as HBPLUS prints the same interaction twice by exchanging the role (hydrogen bond donor as well as 
# acceptor) of interacting atoms.
def uq_interactions(set1):
    extra = []
    for h in range(len(set1)):
        for i in range(h+1,len(set1)):
            if (set1[h][:27] == set1[i][:27]):
                extra.append(set1[h])
    for h in extra:
        if h in set1:
            set1.remove(h)

# List of nucleotides and amino acids.
nucleotides = ['-  A', '-  C', '-  G', '-  U']
amino_acid = ['-GLY', '-ALA', '-SER', '-THR', '-CYS', '-VAL', '-LEU', '-ILE', '-MET', '-PRO', '-PHE', '-TYR',
              '-TRP', '-ASP', '-GLU', '-ASN', '-GLN', '-HIS', '-LYS', '-ARG']

# Look for output files of HBPLUS (.hb2) present in the current directory.
files_hb2 = []
path = os.getcwd()
directory = os.listdir(path)  
for fis in directory: 
    if fis.find('.hb2') >= 0:
        files_hb2.append(fis)
files_hb2.sort()

# Analyzing each .hb2 file recursively to identify water bridges.
for f in files_hb2:
    file = open(f, 'r') # Read .hb2 files
    data = file.readlines()
    hb_water = [] # Created a list of hydrogen bonds of amino acids and nucleotides with water molecules.
    new_data = [] # Created a list of all direct hydrogen bonds between amino acids and nucleotides.
    
    for l in range(len(data)):
        # Rearranging the format of writing hydrogen bonds of water molecules with amino acids or nucleotides; 
        # information of water molecules will be written first followed by amino acid or nucleotide 
        # (A2601-HOH O   A0018-ASN N   3.28).  
        if data[l].count('-HOH') == 1:
            p1 = data[l][:14]
            p2 = data[l][14:28] 
            p3 = data[l][28:33]
            if 'HOH' in p1 and p2[5:9] in nucleotides or 'HOH' in p1 and p2[5:9] in amino_acid:
                r = p1 + p2 + p3
                hb_water.append(r.strip())
            if 'HOH' in p2 and p1[5:9] in nucleotides or 'HOH' in p2 and p1[5:9] in amino_acid: 
                r = p2 + p1 + p3
                hb_water.append(r.strip())
            
        # Rearranging the format of writing direct hydrogen bonds between amino acids and nucleotides; 
        # information of nucleotide will be written first followed by amino acid (C0105-  G N7  A0043-ASN N   2.90). 
        if data[l].count('-HOH') == 0:
            p1 = data[l][:14]
            p2 = data[l][14:28] 
            p3 = data[l][28:33]
            if 'HOH' not in p1 and 'HOH' not in p2:
                if p1[5:9] in nucleotides and p2[5:9] in amino_acid:
                    ra = p1 + p2 + p3
                    if ra not in new_data: new_data.append(ra.strip())
                if p2[5:9] in nucleotides and p1[5:9] in amino_acid:
                    ra = p2 + p1 + p3
                    if ra not in new_data: new_data.append(ra.strip())
                        
    # Removing redundant hydrogen bonds arising due to the dual nature of some atoms.
    uq_interactions(new_data) # This will remove repetitions from the list 'new_data'.     
    uq_interactions(hb_water)  # This will remove repetitions from the list 'hb_water'.
    
    wtr = [] # Created a list of unique water molecules using their identity as per PDB record.
    for i in hb_water:
        if i[:13].strip() not in wtr:
            wtr.append(i[:13].strip())
    
    # Sorting all hydrogen bonds of water molecules and placing all hydrogen bonds of particular water adjacent to each other
    # to each other.
    wtr.sort()
    sorted_hbs = []
    for w1 in wtr:
        for w2 in hb_water:
            if w1 in w2:
                sorted_hbs.append(w2)
                
    # Grouping all hydrogen bonds of a particular water molecule, resulting in a water-mediated motif of amino acids 
    # and nucleotides.
    all_inter_water = [] # a list consisting of a list of all hydrogen bonds of water with amino acids and nucleotides. 
    iterator = itertools.groupby(sorted_hbs, lambda string: string.split('H O   ')[0])
    
    # Appending the group by converting it into a list;
    # here 'element' is information of water molecule, on the basis of which all hydrogen bonds of a particular 
    # water molecules are grouped and 'group' is all interaction of that water molecule. 
    for element, group in iterator:
        all_inter_water.append(list(group))
    all_inter_water_joined = []
    for i in all_inter_water:
        all_inter_water_joined.append(" --- ".join(i))
        
    # Improving the output of the code.
    result_1 = [] # list of grouped hydrogen bonds of each water molecule. 
    for i in all_inter_water_joined:
        x = i.split(i[:14])
        xx = ''.join(x)
        xxx = i[:14].strip() + ' --- ' + xx
        result_1.append(xxx)
    
    # Filtering out false water bridges (each water should form at least one hydrogen bond with amino acid and nucleotide).
    r1 = re.compile(".*-  [A,C,G,U] .*")
    newlist1 = list(filter(r1.match, result_1))
    r2 = re.compile(".*(GLY|ALA|SER|THR|CYS|VAL|LEU|ILE|MET|PRO|PHE|TYR|TRP|ASP|GLU|ASN|GLN|HIS|LYS|ARG).*")
    wtr_brg = list(filter(r2.match, newlist1))
    
    # Adding more information to the water bridge; whether cyclic or acyclic.
    # For this, hydrogen bonds of amino acids and nucleotides involved in water bridge formation will be searched
    # in previously created list 'new_data'.
    my_dict = {}
    key = []
    val = []
    for i in wtr_brg:
        NB = [] # List of nucleotides forming hydrogen bonds with water.
        AA = [] # List amino acids forming hydrogen bonds with water.
        for a in range(16,len(i),23):
            if i[a:a+9] not in NB and i[a:a+9][5:] in nucleotides: 
                NB.append(i[a:a+9])
            if i[a:a+9] not in AA and i[a:a+9][5:] in amino_acid: 
                AA.append(i[a:a+9])   
        for n in range(len(NB)):
            for m in range(len(AA)):
                for l in (new_data): 
                    if NB[n] in l and AA[m] in l:
                        key.append(i)
                        val.append(l[:33])
                    
        if i not in key:
            key.append(i)
            val.append('NIL')
            
    for i in range(len(key)):
        for j in range(len(val)):
            if i == j: 
                my_dict.setdefault(key[i], []).append(val[j])
                
    nucleobase_atoms = ['N9', 'N6', 'N2', 'N7', 'O4', 'O6', 'N1', 'N4', 'N3', 'O2']
    
    # Generate output files, here we generated three output files 
    print(('********************  ' + f + '  ********************'), file=open("waterbridges.txt", "a"))
    #print(('********************  ' + f + '  ********************'), file=open("waterbridges_Base.txt", "a"))
    #print(('********************  ' + f + '  ********************'), file=open("waterbridges_RiboPhos.txt", "a"))
    
    
    #for a, b in my_dict.items():
    #
    #    z = 0
    #    for xa in range(26, len(a), 23):
    #        if (a[xa:xa+3].strip()) in nucleobase_atoms:
    #            z += 1
    #    if z >= 1:
    #        print(a,b, file=open("waterbridges_Base.txt", "a"))
    #    if z == 0:
    #        print(a,b, file=open("waterbridges_RiboPhos.txt", "a"))  
    #print('........................................................................ \n', file=open("waterbridges_Base.txt", "a"))
    #print('........................................................................ \n', file=open("waterbridges_RiboPhos.txt", "a"))
   
    
    for a, b in my_dict.items():
        print(a,b, file=open("waterbridges.txt", "a"))

    print('........................................................................ \n', file=open("waterbridges.txt", "a"))
