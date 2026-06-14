#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:44:31 2025

@author: mozhganoroujlu
"""

import os
import cooler
import pandas as pd
from tqdm import tqdm  # For progress bar

# Set directories (adjust these paths as needed)
cool_dir = '/Users/mozhganoroujlu/Desktop/MOZHGUN/cell_fate/hi_c/paper_pipline/cool_accurate_single_cell'  # Directory containing the 6223 .cool files
raw_txt_dir = '/Users/mozhganoroujlu/Desktop/MOZHGUN/cell_fate/hi_c/paper_pipline/raw_txt'  # Directory to save raw .txt files for R input

# Create output directory if it doesn't exist
os.makedirs(raw_txt_dir, exist_ok=True)

# List all .cool files
cool_files = [f for f in os.listdir(cool_dir) if f.endswith('.cool')]

# Process each .cool file
for cool_file in tqdm(cool_files, desc="Processing .cool files"):
    # Load the Cooler file
    clr = cooler.Cooler(os.path.join(cool_dir, cool_file))
    
    # Since only chr1 intra-contacts, fetch pixels for chr1
    pixels = clr.pixels().fetch('chr1')  # Returns DataFrame with 'bin1_id', 'bin2_id', 'count'
    
    # Assuming bin1_id < bin2_id; add chrom columns
    pixels['chrom1'] = 'chr1'
    pixels['chrom2'] = 'chr1'
    
    # Reorder columns: chrom1, bin1_id, chrom2, bin2_id, count
    # Note: bin_ids are 0-based; if you need 1-based, add +1 here
    # pixels['bin1_id'] += 1  # Uncomment if 1-based bins are needed
    # pixels['bin2_id'] += 1
    output_df = pixels[['chrom1', 'bin1_id', 'chrom2', 'bin2_id', 'count']]
    
    # Save to .txt file (tab-separated, no header, no index)
    cell_name = os.path.splitext(cool_file)[0]  # Use file name as cell identifier without .cool
    output_path = os.path.join(raw_txt_dir, f"{cell_name}.txt")
    output_df.to_csv(output_path, sep='\t', header=False, index=False)
    
print(f"Processed {len(cool_files)} .cool files and saved raw .txt files to {raw_txt_dir}")