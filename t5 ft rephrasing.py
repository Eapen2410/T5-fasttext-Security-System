from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")
from peft import LoraConfig, TaskType

peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q", "v"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.SEQ_2_SEQ_LM,

)
def preprocess(example):
    inputs = tokenizer(example["input_text"], padding="max_length", truncation=True, max_length=64, return_tensors="pt")
    targets = tokenizer(example["target_text"], padding="max_length", truncation=True, max_length=64, return_tensors="pt")
    return {
        "input_ids": inputs.input_ids[0],
        "attention_mask": inputs.attention_mask[0],
        "labels": targets.input_ids[0]
    }

tokenized_dataset = dataset.map(preprocess)

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    num_train_epochs=6,
    logging_steps=10,
    save_strategy="no",
    eval_strategy="no",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

trainer.train()