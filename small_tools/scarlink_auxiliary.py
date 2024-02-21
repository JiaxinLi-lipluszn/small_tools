import pandas as pd

def hic_shapley(hic_chr=None,
                hic_range=None,
                hic_idx=None,
                hic_resolution=1e4,
                tile_df=None,
                gene=None,
                tile_resolution=500,
                condition_function=None):
    '''
    A function to subset scarlink's result dataframe to obtain all bins in a hic bin
    '''
    tile_df = tile_df.loc[tile_df['gene']==gene,:]

    if hic_range is None and hic_idx is None:
        raise ValueError("At least one of hic_range and hic_idx should be not None")
    
    # Filter the tile df by some condiiton, could be FDR or p value threshold
    if condition_function is not None:
        filtered_tile_df = tile_df[condition_function(tile_df)]
    else:
        filtered_tile_df = tile_df
    
    
    # Get the corresponding tiles
    if hic_range is None:
        hic_range = (hic_idx * hic_resolution, (hic_idx + 1) * hic_resolution)
    
    filtered_tile_df = filtered_tile_df[(filtered_tile_df['chr']==hic_chr) & (filtered_tile_df['start'] < hic_range[1]) & (filtered_tile_df['end'] > hic_range[0])]
    # print(filtered_tile_df)
    return(filtered_tile_df)
