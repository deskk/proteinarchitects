import os

input_folder = os.path.join(shared_path, 'fulldataset')
output_folder = os.path.join(shared_path, 'modifiedfasta')
for fasta_file in files_folder:
  input_file = input_folder + '/' + fasta_file
  output_file = output_folder + '/' + fasta_file
  modify_fasta_headers(input_file, output_file)
