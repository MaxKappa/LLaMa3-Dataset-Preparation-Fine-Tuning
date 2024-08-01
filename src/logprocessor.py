import os
import random
import pandas as pd
import json

class LogProcessor:
    def __init__(self, dir, batch_chars, selector, percentage):
        self.dir = dir
        self.training_file_path = os.path.join(self.dir, "training.jsonl")
        self.test_file_path = os.path.join(self.dir, "test.jsonl")
        self.output_file_path = os.path.join(self.dir, "all_data.jsonl")
        self.batch_chars = batch_chars
        self.selector = selector
        self.percentage = percentage
        self.count = 0
        print('Starting dataset creation...')
        open(self.training_file_path, 'w').close()
        open(self.output_file_path, 'w').close()
        open(self.test_file_path, 'w').close()

    def percentage_count(self, total):
        return int((self.percentage * total) / 100.0)

    def split_logs_to_batches(self, logs):
        """Split logs into batches based on character count."""
        batches = []
        current_batch = []
        current_char_count = 0

        for log in logs:
            log_chars = len(log)
            if current_char_count + log_chars > self.batch_chars:
                batches.append(current_batch)
                current_batch = [log]
                current_char_count = log_chars
            else:
                current_batch.append(log)
                current_char_count += log_chars

        if current_batch:
            batches.append(current_batch)

        return batches

    def process_files(self):
        """Process all JSON files in the input directory."""
        for subdir, _, files in os.walk(self.dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(subdir, file)
                    self.process_file(file_path)


    def process_file(self, file_path):
        """Process a single JSON file."""
        log_df = pd.read_json(file_path)
        log_df['pid'] = log_df['pid'].fillna(0).astype(int)
        logs = log_df.apply(lambda row: ', '.join(row.values.astype(str)), axis=1).tolist()
        batches = self.split_logs_to_batches(logs)
        self.create_jsonl(batches)
        print(f"File successfully processed {file_path}")

    def create_jsonl(self, batches):
        """Create a JSONL file from batches of logs."""
        jsonl_data = [
            {
            "messages": [
                    {"role": "system", "content": "Determine whether malware activity is detected in this piece of the log. The format is pid, filename, operation. If operation is not present the filename is the thread started. The operation letters are: CreateFile : C, ReadFile: R, DeleteFile: D, WriteFile: W, RegSetValue: SV, RegCreateKey: CK, RegDeleteKey: DK, RegDeleteValue: DV"
                    },
                    {"role": "user", "content": "\n".join(batch)},
                    {"role": "assistant", "content": 'No' if self.selector else 'Yes'}
                ]
            }
            for batch in batches
        ]
        with open(self.output_file_path, 'a') as jsonl_file:
            for entry in jsonl_data:
                json.dump(entry, jsonl_file)
                jsonl_file.write('\n')
    
    def split_jsonl_file(self):
        with open(self.output_file_path, 'r') as file:
            lines = file.readlines()
        json_objects = [json.loads(line) for line in lines]
        training_count = self.percentage_count(len(json_objects))
        random.shuffle(json_objects)
        
        first_file_batches = json_objects[:training_count]
        second_file_batches = json_objects[training_count:]
        
        with open(self.training_file_path, 'a') as file1:
            json.dump(first_file_batches, file1)
            file1.write('\n')
        
        with open(self.test_file_path, 'a') as file2:
            json.dump(second_file_batches, file2)
            file2.write('\n')
        

