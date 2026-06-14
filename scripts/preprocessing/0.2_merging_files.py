import gzip
import os

def merge_pairs_gz_dedup_headers(file1_name, file2_name, output_name):
    """
    Merge two .pairs.gz files into a single .pairs.gz file, deduplicating headers.
    Assumes files are in the current working directory.
    
    Args:
        file1_name (str): Name of the first .pairs.gz file
        file2_name (str): Name of the second .pairs.gz file
        output_name (str): Name of the output merged .pairs.gz file
    """
    try:
        # Check if files exist in the current directory
        if not os.path.exists(file1_name):
            raise FileNotFoundError(f"File {file1_name} not found in the current directory")
        if not os.path.exists(file2_name):
            raise FileNotFoundError(f"File {file2_name} not found in the current directory")

        # Store unique headers while preserving order
        headers = []
        header_set = set()
        data_lines = []

        # Process both files
        for file_name in [file1_name, file2_name]:
            with gzip.open(file_name, 'rt') as f:
                for line in f:
                    if line.startswith('#'):
                        # Add header if not already seen
                        if line not in header_set:
                            headers.append(line)
                            header_set.add(line)
                    else:
                        # Collect data lines
                        data_lines.append(line)

        # Write output: headers followed by data
        with gzip.open(output_name, 'wt') as out:
            # Write deduplicated headers
            for header in headers:
                out.write(header)
            # Write data lines
            for data_line in data_lines:
                out.write(data_line)

        print(f"Successfully merged {file1_name} and {file2_name} into {output_name} with deduplicated headers")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

# Option 1: Hardcode file names (uncomment and edit these lines to use)
file1_name = "462_filtered_chr1_barcodes.pairs.gz"
file2_name = "716_filtered_chr1_barcodes.pairs.gz"
output_name = "merged_716_462_chr1.pairs.gz"


# Run the merge function
merge_pairs_gz_dedup_headers(file1_name, file2_name, output_name)
