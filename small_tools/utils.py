import pandas as pd
from importlib_resources import files
import data

def load_data(data_key):
    # Use importlib.resources to construct path
    ret_path = None
    if data_key ==  "hg38_tss":
        ret_path = files(data).joinpath('hg38.tss.symbol.promoters.tsv')
    return ret_path

def compare_ranges(rg1, rg2):
    '''
    Compare if two ranges overlaps
    Inputs:
    rg1: (start1, end1), a turple indicating the ragne 1
    rg2: (start2, end2), a turple indicating the ragne 2
    return True if the two ranges overlap
    '''
    start1, end1 = sorted(rg1)  # Ensure the range is properly ordered
    start2, end2 = sorted(rg2)  # Ensure the range is properly ordered
    if (start1 <= end2 and start2 <= end1):
        return True
    else:
        return False
    

def find_promoter_bin(gene, 
                      genome='hg38', 
                      hic_resolution=1e4, 
                      promoter_upstream=1000,
                      promoter_downstream=100):
    '''
    # TODO: consider the chromosome size
    # TODO: consider the case that the promoter region length is larger than hic resolution
    A function to define the Hi-C bin that containing the specific gene's promoter region
    Parameters:
    gene: gene name, # TODO: could be a list
    genome: genome version to use, default hg38, make sure your hic data was also processed in the same genome version
    hic_resolution: the resolution of the hic interactions
    Return:
    (start, end) of the bin that contains the gene's promoter
    '''
    # Get the gene's different transcripts
    tss_file = load_data(f"{genome}_tss")
    print(f"Loading genome {genome} tss information from {tss_file}")

    tss_df = pd.read_csv(tss_file, sep = '\t')
    gene_tx_df = tss_df.loc[tss_df['gene_symbol'] == gene, :]

    # Define the promoter region for each transcripts (each line)
    promoter_coor_1 = []
    promoter_coor_2 = []
    for i, row in gene_tx_df.iterrows():
        if row['strand'] == '+':
            promoter_coor_1.append(row['start'] - promoter_upstream)
            promoter_coor_2.append(row['start'] + promoter_downstream)
        elif row['strand'] == '-':
            promoter_coor_1.append(row['end'] - promoter_downstream)
            promoter_coor_2.append(row['end'] + promoter_upstream)
        else:
            print(f"Error: the strand information of gene {gene}, transcript {row['tx_name']} is missing, reported strand is {row['strand']}")
    
    bin_dict = {}
    for i in range(len(promoter_coor_1)):
        bin_idx_1 = promoter_coor_1[i] // hic_resolution
        bin_idx_2 = promoter_coor_2[i] // hic_resolution
        if bin_idx_1 == bin_idx_2:
            # In this case, both end of the promoter are in the same bin
            bin_dict[bin_idx_1] = bin_dict.get(bin_idx_1, 0) + promoter_upstream + promoter_downstream
        else:
            # In this case, the promoter region is sitting on the boundary of a hic bin
            bin_dict[bin_idx_1] = bin_dict.get(bin_idx_1, 0) + ((bin_idx_1 + 1) * hic_resolution - promoter_coor_1[i])
            bin_dict[bin_idx_2] = bin_dict.get(bin_idx_2, 0) + (promoter_coor_2[i] - (bin_idx_2 * hic_resolution))
    # print(bin_dict)
    max_key = max(bin_dict, key = bin_dict.get)
    return(int(max_key * hic_resolution),int((max_key + 1) * hic_resolution) )