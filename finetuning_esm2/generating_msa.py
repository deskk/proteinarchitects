from Bio import SeqIO
from Bio.Align.Applications import MuscleCommandline
import os

def generate_msa_with_muscle(input_fasta, output_msa):
    muscle_cline = MuscleCommandline(input=input_fasta)
    muscle_cline.set_parameter("out", output_msa)


    stdout, stderr = muscle_cline()

def main():

    input_dir = "/content/drive/MyDrive/fulldataset/fulldataset"

    # Output directory for saving the MSA files
    output_dir = "/content/drive/MyDrive/MSA_dataset"


    os.makedirs(output_dir, exist_ok=True)


    for file_name in os.listdir(input_dir):
        if file_name.endswith(".fasta"):
            fasta_file = os.path.join(input_dir, file_name)

            output_msa = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.msa")
            generate_msa_with_muscle(fasta_file, output_msa)

if __name__ == "__main__":
    main()
