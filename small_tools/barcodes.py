import pandas as pd

def process_barcode(barcode, **kwargs):
    """
    Process a cell barcode and extract its main body, lane number, and suffix.
    You can define the separators by input them into **kwargs

    Parameters:
    barcode (str): The cell barcode
    seps (list): a list of separators in order
    parts (list): a list of names of parts in order

    Returns:
    tuple: a dictionary of all parts in the barcode.

    Example Usage:
    params = {
    "seps" : ['#', '-'],
    "parts" :['lane', 'barcode', 'suffix']
    }

    archR_barcodes_sep = df['x'].apply(lambda x: pd.Series(process_barcode(barcode=x, **params)))

    """
    assert("seps" in kwargs.keys() and "parts" in kwargs.keys())
    assert(len(kwargs['seps']) == len(kwargs['parts']) - 1)

    ret_dic = {}

    for i, sep in enumerate(kwargs['seps']):
        parts = barcode.split(sep, 1)
        ret_dic[kwargs['parts'][i]] = parts[0]
        barcode = parts[1]
    
    ret_dic[kwargs['parts'][-1]] = barcode

    return ret_dic