import torch

input_sequence = "MSGPVPSRARVYTDVNTHRPREYWDYESHVVEWGNQDDYQLVRKLGRGKYSEVFEAINITNNEKVVVKILKPVKKKKIKREIKILENLRGGPNIITLADIVKDPVSRTPALVFEHVNNTDFKQLYQTLTDYDIRFYMYEILKALDYCHSMGIMHRDVKPHNVMIDHEHRKLRLIDWGLAEFYHPGQEYNVRVASRYFKGPELLVDYQMYDYSLDMWSLGCMLASMIFRKEPFFHGHDNYDQLVRIAKVLGTEDLYDYIDKYNIELDPRFNDILGRHSRKRWERFVHSENQHLVSPEALDFLDKLLRYDHQSRLTAREAMEHPYFYTVVKDQARMGSSSMPGGSTPVSSANMMSGISSVPTPSPLGPLAGSPVIAAANPLGMPVPAAAGAQQLEHHHHHH"


region_start = 150
region_end = 200

num_sequences_to_generate = 5
max_masking_steps = 100
generated_sequences = []

for _ in range(num_sequences_to_generate):
    new_sequence = input_sequence

    for _ in range(max_masking_steps):
        tokens = tokenizer(new_sequence, return_tensors="pt")
        num_tokens = len(tokens.input_ids[0])
        masking_prob = 0.15


        valid_indices = [i for i in range(region_start, region_end + 1)]
        masked_idx = torch.randint(len(valid_indices), (1,)).item()
        masked_idx = valid_indices[masked_idx]

        tokens.input_ids[0, masked_idx] = tokenizer.mask_token_id

        with torch.no_grad():
            outputs = model(**tokens)

        predicted_token_id = torch.argmax(outputs.logits, dim=-1)[0, masked_idx]

        new_sequence = new_sequence[:masked_idx] + tokenizer.decode(predicted_token_id.item()) + new_sequence[masked_idx + 1:]

    generated_sequences.append(new_sequence)

for i, sequence in enumerate(generated_sequences):

    sequence = sequence.replace("<cls>", "").replace("<sep>", "")


    sequence = " ".join(sequence.strip().split())

    print(f"Generated Sequence {i + 1}:", sequence)
