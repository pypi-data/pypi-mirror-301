import os
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from torch.utils.data import Dataset
import gc
from sklearn.model_selection import train_test_split

# Set CUDA launch blocking for detailed error tracking
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

class InfoExtractionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, task_instruction, max_length=1024):
        self.inputs = []
        self.labels = []
        
        for text, label in zip(texts, labels):
            input_text = f"{task_instruction}: {text}"
            inputs = tokenizer(input_text, padding='max_length', truncation=True, max_length=max_length, return_tensors="pt")
            labels = tokenizer(label, padding='max_length', truncation=True, max_length=max_length, return_tensors="pt").input_ids
            self.inputs.append(inputs['input_ids'].squeeze(0))
            self.labels.append(labels.squeeze(0))

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return {'input_ids': self.inputs[idx], 'labels': self.labels[idx]}

class InfoExtractionModel:
    def __init__(self, model_name='t5-small', cache_dir=None):
        self.model_name = model_name
        self.cache_dir = cache_dir or os.getcwd()
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=self.cache_dir).to(self.device)

    def train(self, texts_train, labels_train, texts_eval, labels_eval, task_instruction, num_epochs, output_dir='./info_extraction_model'):
        print(f"Training the model for task: {task_instruction} for {num_epochs} epoch(s)")
        train_dataset = InfoExtractionDataset(texts_train, labels_train, self.tokenizer, task_instruction)
        eval_dataset = InfoExtractionDataset(texts_eval, labels_eval, self.tokenizer, task_instruction)

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,  # Use the user-defined number of epochs
            per_device_train_batch_size=1,
            save_steps=500,
            save_total_limit=2,
            evaluation_strategy="epoch",
            logging_dir='./logs',
            learning_rate=5e-5,  
            report_to="none"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        trainer.train()
        self.model.save_pretrained(output_dir)
        print(f"Model trained and saved to {output_dir}")

        del train_dataset, eval_dataset, trainer, training_args
        torch.cuda.empty_cache()
        gc.collect()

    def load_model(self, model_dir):
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir).to(self.device)
        print(f"Model loaded from {model_dir}")

    def extract(self, text, task_instruction):
        print(f"Extracting information based on task: {task_instruction}")
        input_text = f"{task_instruction}: {text}"
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, max_length=1024).to(self.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=150,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id
            )

        extracted_info = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        print(f"Extracted information: {extracted_info}")
        
        del inputs, output_ids
        torch.cuda.empty_cache()
        gc.collect()

        return extracted_info

    def evaluate_test_set(self, texts_test, labels_test, task_instruction, output_file):
        extracted_info = []
        for text in texts_test:
            extracted_info.append(self.extract(text, task_instruction))

        results_df = pd.DataFrame({
            'Text': texts_test,
            'True Info': labels_test,
            'Extracted Info': extracted_info
        })

        results_df.to_excel(output_file, index=False)
        print(f"Test set results saved to {output_file}")

# Sample usage with print statements
if __name__ == "__main__":
    # Initialize the extraction model
    extractor = InfoExtractionModel()

    # Load your dataset
    dataset = pd.read_excel('/kaggle/working/updated_s2orc_small_with_authors.xlsx')  # Replace with actual path

    # Step 1: Show available columns and ask user for input
    print("\n--- Available Columns in Dataset ---")
    print(dataset.columns)

    # Ask the user to provide the column names for text and labels
    text_column = input("\nEnter the name of the column containing the text (e.g., 'combined_text'): ")
    label_column = input("Enter the name of the column containing the labels (e.g., 'Authors'): ")

    # Step 2: Define task instruction
    print("\n--- Example Task Scenarios ---")
    print("1. Extract Authors")
    print("2. Extract Publication Dates")
    print("3. Extract Keywords")
    print("4. Extract Abstract")
    print("Choose the task you want to perform.")
    
    task_instruction = input("Enter your task (e.g., 'Extract authors', 'Extract keywords'): ")
    print(f"You chose: {task_instruction}")

    # Ask the user for the number of epochs
    num_epochs = int(input("\nHow many epochs would you like to train for? (e.g., 3, 5, 10): "))
    print(f"Training for {num_epochs} epoch(s).")

    # Use the column names provided by the user
    texts = dataset[text_column].tolist()
    labels = dataset[label_column].tolist()

    # Split dataset into training (80%), validation (10%), and test (10%) sets
    texts_train, texts_eval, labels_train, labels_eval = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Step 3: Train the model with user-defined epochs
    extractor.train(texts_train, labels_train, texts_eval, labels_eval, task_instruction, num_epochs)

    # Step 4: Load the trained model
    extractor.load_model('./info_extraction_model')

    # Step 5: Evaluate the test set
    print("\n--- Answer ---")
    new_text_default = "Complete resolution of cutaneous larva migrans with topical ivermectin: A case report Francesca  Magri, Camilla  Chello, Giulia  Pranteda, Guglielmo  Pranteda Cutaneous larva migrans (CLM; also called creeping eruption) is a cutaneous ectoparasitosis commonly observed in tropical countries."
    new_text = input("Enter the text or press Enter to use default value: ") or new_text_default
    extractor.extract(new_text, task_instruction)

    # Clear memory after the process
    del texts_train, labels_train, texts_eval, labels_eval, dataset
    torch.cuda.empty_cache()
    gc.collect()
