import os
import pandas as pd


def save_batch_result_and_concat(dataframe, batch_index, batch_path = None):
    """
    Function to save the accumulated processed batches as a single CSV file.
    """
    if batch_path:
        functions_dir = os.path.abspath(batch_path)
    
    else:
        functions_dir = os.path.join(os.getcwd(), 'generated_data', 'batches')

    # Ensure the folder exists
    os.makedirs(functions_dir, exist_ok=True)
    
    # Save the concatenated DataFrame
    concat_filepath = os.path.join(functions_dir, f'batch_{batch_index}.csv')
    dataframe.to_csv(concat_filepath, index=False, mode='w')
    print(f"Concatenated batches for index {batch_index} saved to {concat_filepath}.")


def save_final(dataframe, data_frame_path = None):
    """
    Function to save the final DataFrame to a CSV file.
    """
    # Ensure the directory exists, create it if it doesn't
    if data_frame_path:
        directory = os.path.dirname(os.path.abspath(data_frame_path))
        path = os.path.join(directory, 'final_csv.csv')
    else:
        directory = os.path.join(os.getcwd(), 'generated_data', 'dataframe')
        path = os.path.join(directory, 'final_csv.csv')
    os.makedirs(directory, exist_ok=True)

    # Save the DataFrame to CSV, overwrite if the file already exists
    dataframe.to_csv(path, index=False, mode='w')
    print(f"Final DataFrame saved to {path}.")  # Print a confirmation message
