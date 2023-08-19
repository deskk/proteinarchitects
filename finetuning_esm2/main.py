import yaml
from dataset import SequenceDataset, read_fasta_files
from model import train_model

with open('config.yaml') as file:
    config = yaml.full_load(file)

fasta_folder_path = config['fasta_folder_path']
sequences = read_fasta_files(fasta_folder_path)

train_model(sequences)