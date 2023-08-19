import yaml
import torch
from dataset import SequenceDataset
from transformers import AutoTokenizer, EsmForMaskedLM
from sklearn.model_selection import train_test_split
from transformers import TrainingArguments, DataCollatorForLanguageModeling, Trainer

def train_model(sequences):
    with open('config.yaml') as file:
        config = yaml.full_load(file)

    tokenizer = AutoTokenizer.from_pretrained(config['model']['pretrained_model'])
    model = EsmForMaskedLM.from_pretrained(config['model']['pretrained_model'])
    train_sequences, val_sequences = train_test_split(sequences, test_size=0.2, random_state=42)
    train_dataset = SequenceDataset(train_sequences, tokenizer)
    val_dataset = SequenceDataset(val_sequences, tokenizer)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=config['model']['mlm_probability'])

    training_args = TrainingArguments(
        output_dir=config['training']['output_dir'],
        evaluation_strategy=config['training']['evaluation_strategy'],
        save_strategy=config['training']['save_strategy'],
        num_train_epochs=config['training']['num_train_epochs'],
        per_device_train_batch_size=config['training']['per_device_train_batch_size'],
        save_steps=config['training']['save_steps'],
        save_total_limit=config['training']['save_total_limit'],
        learning_rate=config['training']['learning_rate'],
        warmup_steps=config['training']['warmup_steps'],
        weight_decay=config['training']['weight_decay'],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    trainer.train()