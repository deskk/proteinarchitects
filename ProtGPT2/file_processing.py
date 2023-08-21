def modify_fasta_headers(input_file, output_file):
  with open(input_file,'r') as f:
    lines = f.readlines()

  modified_lines = []
  for line in lines:
    if line.startswith('>'):
      modified_lines.append("<|endoftext|>")
    else:
      modified_lines.append(line)

  with open(output_file, 'w') as f:
    f.writelines(modified_lines)
