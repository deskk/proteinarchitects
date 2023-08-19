import os
import torch
from torch.utils.data import Dataset

def read_fasta_files(fasta_folder_path):
    fasta_data = []
    for filename in os.listdir(fasta_folder_path):
        file_path = os.path.join(fasta_folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as fasta_file:
                lines = fasta_file.readlines()
                label = lines[0].strip()
                sequence = "".join(line.strip() for line in lines[1:])
                fasta_sequence = (label[1:], sequence)
                fasta_data.append(fasta_sequence)
    return fasta_data

class SequenceDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        label, sequence = self.data[idx]
        inputs = self.tokenizer(sequence, return_tensors='pt', max_length=1024, padding='max_length', truncation=True)
        inputs = {key: value.squeeze() for key, value in inputs.items()}
        inputs['labels'] = inputs['input_ids'].detach().clone()
        rand = torch.rand(inputs['input_ids'].shape)
        mask_arr = (rand < 0.15) * (inputs['input_ids'] != 0)
        selection = torch.flatten(mask_arr.nonzero()).tolist()
        inputs['input_ids'][selection] = self.tokenizer.mask_token_id
        inputs['attention_mask'] = (inputs['input_ids'] > self.tokenizer.pad_token_id).float()
        return inputs