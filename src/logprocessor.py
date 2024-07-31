import os
import pandas as pd
import json


class LogProcessor:
    def __init__(self, input_dir, batch_chars):
        self.input_dir = input_dir
        self.output_dir = f"{input_dir}_FT"
        self.batch_chars = batch_chars
        print('Starting dataset creation...')
        os.makedirs(self.output_dir, exist_ok=True)

    def load_json_to_df(self, file_path):
        """Load JSON data from a file into a DataFrame."""
        return pd.read_json(file_path)

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
        for subdir, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(subdir, file)
                    self.process_file(file_path, subdir)

    def process_file(self, file_path, subdir):
        """Process a single JSON file."""
        log_df = self.load_json_to_df(file_path)
        log_df['pid'] = log_df['pid'].fillna(0).astype(int)
        logs = log_df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist()
        batches = self.split_logs_to_batches(logs)
        self.create_jsonl(batches, file_path)

    def create_jsonl(self, batches, original_file_path):
        """Create a JSONL file from batches of logs."""
        jsonl_data = [
            {
                "messages": [
                    {"role": "system", "content": "Determine whether malware activity is detected in this piece of the log."},
                    {"role": "user", "content": batch}
                ]
            }
            for batch in batches
        ]

        relative_path = os.path.relpath(original_file_path, self.input_dir)
        relative_path_without_ext = os.path.splitext(relative_path)[0]
        jsonl_file_path = os.path.join(self.output_dir, f"{relative_path_without_ext}.jsonl")
        os.makedirs(os.path.dirname(jsonl_file_path), exist_ok=True)

        with open(jsonl_file_path, 'w') as jsonl_file:
            for entry in jsonl_data:
                json.dump(entry, jsonl_file)
                jsonl_file.write('\n')
        print(f"Dataset JSONL salvato in: {jsonl_file_path}")