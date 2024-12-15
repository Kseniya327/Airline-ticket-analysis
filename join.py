import pandas as pd
import os
import glob

def combine_csv_files(input_dir, output_file):
    """
    Combines multiple CSV files from a directory into a single CSV file.
    This version adds more robust error handling and verbose output.

    Args:
        input_dir: The directory containing the CSV files.
        output_file: The path to the output CSV file.

    Returns:
        None
    """
    print(f"Starting CSV combination in directory: {input_dir}")


    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' is not a valid directory.")
        return

    all_files = glob.glob(os.path.join(input_dir, "*.csv"))
    if not all_files:
        print(f"Error: No CSV files found in directory: {input_dir}")
        return
    print(f"Found {len(all_files)} CSV files in directory")

    all_dataframes = []

    for file_path in all_files:
        print(f"Processing file: {file_path}")
        print(f"  Trying to read from absolute path {os.path.abspath(file_path)}")  #<--Added print
        try:
            df = pd.read_csv(file_path)
            print(f"  Successfully read {file_path} - shape: {df.shape}")
            all_dataframes.append(df)
        except pd.errors.EmptyDataError:
            print(f"Warning: {file_path} is empty, skipping")
            continue
        except pd.errors.ParserError as pe:
            print(f"Error: Failed to parse file {file_path}: {pe}")
            continue
        except Exception as e:
           print(f"Error reading file {file_path}: {e}")
           continue

    if not all_dataframes:
        print("Error: No valid DataFrames were loaded from the files. Cannot combine.")
        return

    try:
        print("Concatenating all dataframes...")
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"Combined DataFrame shape: {combined_df.shape}")
    except Exception as e:
        print(f"Error during dataframe concatenation: {e}")
        return

    try:
       print(f"Writing combined data to {output_file}")
       combined_df.to_csv(output_file, index=False, encoding='utf-8')
       print(f"Successfully combined CSV files into: {output_file}")
    except Exception as e:
       print(f"Error writing to output file: {e}")


# Example usage:
input_directory = r"D:\МАГистратура\1 КУРС\1 семестр\Большие данные\Анализ ценообразования на авиабилеты\дистрибутив" # Using raw string
output_filename = "all_tickets.csv"
combine_csv_files(input_directory, output_filename)