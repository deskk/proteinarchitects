import random
import pandas as pd
import os

def read_fasta_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = lines[0].rstrip("\n")
    return lines

def prepare_data(input_folder, shared_path, files_folder, new_path):
    fasta_content_list = []
    for fasta_file in files_folder:
        input_file = os.path.join(input_folder, fasta_file)
        output_file = os.path.join(new_path, fasta_file)
        modify_fasta_headers(input_file, output_file)
        
        file_path = os.path.join(new_path, fasta_file)
        modified_lines = read_fasta_file(file_path)
        fasta_content_list.append(modified_lines)

    df = pd.DataFrame(fasta_content_list, columns=['Sequences'])
    return df

def split_train_valid_data(df):
    train_size = round(0.9 * len(df.index))
    train_index = random.sample(range(0, len(df.index)), train_size)
    valid_index = [ind for ind in range(0, len(df.index)) if ind not in train_index]

    train = df.filter(items=train_index, axis=0).reset_index(drop=True)
    valid = df.filter(items=valid_index, axis=0).reset_index(drop=True)
    return train, valid
