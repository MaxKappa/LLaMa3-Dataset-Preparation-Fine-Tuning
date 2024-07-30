import filter, os, mongo, json, csvconverter, argparse
from config import load_config
def main():

    config = load_config()

    parser = argparse.ArgumentParser(description='Data preparation for LLM Fine-Tuning')
    parser.add_argument('--clean', required=False, default=False, action='store_true', help='If you are fetching clean logs')
    parser.add_argument('--csv', required=False, default=False, action='store_true', help='Create a converted CSV files directory')
    parser.add_argument('--path', required=True, help='Path of directory')
    parser.add_argument('--dir_name', required=True, help='Name of output directory')
    parser.add_argument('--hash_filepath', required=False, default=False, action='store_true', help='Hash all filepath in logs')
    args = parser.parse_args()

    output_dir = args.path + args.dir_name  #/Users/massimiliano/Desktop/UNIMI/tesi/data/

    mongo_filter = mongo.Mongo(config['MONGO_URI'], config['DB_NAME'], output_dir, args.clean)
    mongo_filter.process_collections()

    data_filter = filter.Filter(hash=args.hash_filepath)
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            datatype = file.split('.')[0]
            file_path = os.path.join(root, file)
            data_filter.filter_data(datatype, file_path)

    if args.csv == True:
        converter = csvconverter.CSVConverter(output_dir)
        converter.convert()
if __name__ == "__main__":
    main()
