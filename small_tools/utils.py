
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