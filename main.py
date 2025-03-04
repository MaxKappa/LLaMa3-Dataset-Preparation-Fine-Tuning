import os, json, argparse
import src.filter as filter
import src.mongo as mongo
import src.csvconverter as csvconverter
import src.logprocessor as logprocessor
from config import load_config
def main():

    config = load_config()

    parser = argparse.ArgumentParser(description='Data preparation for LLM Fine-Tuning')
    parser.add_argument('--csv', required=False, default=False, action='store_true', help='Create a converted CSV files directory')
    parser.add_argument('--path', required=True, help='Path of directory output, if skip mongodb an existing directory')
    parser.add_argument('--dir_name', required=True, help='Name of output directory')
    parser.add_argument('--hash_filepath', required=False, default=False, action='store_true', help='Hash all filepath in logs')
    parser.add_argument('--skip', required=False, action='store_true', help='Skip database fetch')
    parser.add_argument('--percentage', required=False, default=100, help='Split fine tuning data in 2 blocks of size equal to percentage')
    args = parser.parse_args()

    output_dir = args.path + args.dir_name  #/Users/massimiliano/Desktop/UNIMI/tesi/data/
    if not args.skip:
        mongo_filter = mongo.Mongo(config['MONGO_URI'], config['DB_NAME'], output_dir)
        mongo_filter.process_collections()
    else:
        if not os.path.exists(output_dir):
            raise('Path doesn\'t exists')
        print("Skipping database fetching...")
    data_filter = filter.Filter(hash=args.hash_filepath)
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            datatype = file.split('.')[0]
            file_path = os.path.join(root, file)
            data_filter.filter_data(datatype, file_path)

    if args.csv == True:
        converter = csvconverter.CSVConverter(output_dir)
        converter.convert()
    processor = logprocessor.LogProcessor(output_dir, 12000, int(args.percentage))
    processor.process_files()
    processor.split_jsonl_file()

if __name__ == "__main__":
    main()
