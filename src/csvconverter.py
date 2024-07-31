import os
import pandas as pd

class CSVConverter:
    def __init__(self, source_dir):
        
        self.source_dir = source_dir
        self.target_dir = source_dir + "_CSV"

        if not os.path.exists(self.source_dir):
            raise ValueError("Path non esistente")
        
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        print("Starting conversion...")

    def convert(self):
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.json'):
                    self.convert_file(root, file)

    def convert_file(self, root, file):
        json_path = os.path.join(root, file)

        try:
            df = pd.read_json(json_path)
        except ValueError as e:
            print(f"Errore nella lettura del file JSON {json_path}: {e}")
            return

        relative_path = os.path.relpath(root, self.source_dir)
        target_dir = os.path.join(self.target_dir, relative_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        csv_path = os.path.join(target_dir, file.replace('.json', '.csv'))
        df.to_csv(csv_path, encoding='utf-8', index=False,  float_format='%.0f')
        print(f"File successfully converted: {csv_path}")

