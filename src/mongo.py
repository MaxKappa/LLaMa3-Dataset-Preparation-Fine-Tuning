import json
import os
import re
import time
from pymongo import MongoClient
from bson.json_util import dumps

class Mongo:
    def __init__(self, uri, db_name, output_dir):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.output_dir = output_dir
        self.create_output_dir()

    def create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def retrieve_and_save_data(self, collection_name, pipeline, file_name):
        collection = self.db[collection_name]
        data = list(collection.aggregate(pipeline))
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w') as file:
            file.write(dumps(data))
        return data

    def process_collections(self):
        collections = self.db.list_collection_names()
        print("Fetching from db...")
        count = 0
        for coll in collections:
            if "FIBRATUS" in coll :
                start = time.time()
                count += 1
                hash_value = coll.split('.')[2]
                path = os.path.join(self.output_dir, hash_value)
                os.makedirs(path, exist_ok=True)
                self.retrieve_and_save_data(coll, self.process_pipeline(), os.path.join(path, 'process.json'))
                self.retrieve_and_save_data(coll, self.thread_pipeline(), os.path.join(path, 'thread.json'))
                self.retrieve_and_save_data(coll, self.reg_pipeline(), os.path.join(path, 'reg.json'))
                end = time.time()
                print(f'Directory {hash_value} saved, count: {count}, duration: {end-start}s')       

    def network_pipeline(self):
        return [{'$match': {'name': {'$regex': 'Send|Recv|Connect|Disconnect', '$options': 'i'}, 'kparams.dip': {'$ne': None}}}, {'$project': {'_id': 0, 'pid': '$pid', 'dest': '$kparams.dip', 'prot': '$kparams.l4_proto', 'cmd': '$ps.cmdline', 'op': '$name'}}]

    def process_pipeline(self):
        return [{'$match': {'name': {'$regex': 'ReadFile|CreateFile|WriteFile', '$options': 'i'}, 'kparams.file_name': {'$ne': None}}}, {'$project': {'_id': 0, 'pid': '$pid', 'fname': '$kparams.file_name', 'op': '$name'}}] #'cmd': '$ps.cmdline', 'op': '$name'}}] #Process|Image|File

    def thread_pipeline(self):
        return [{'$match': {'name': {'$regex': 'Thread', '$options': 'i'}, 'kparams.exe': {'$ne': None}}}, {'$project': {'_id': 0, 'pid': '$pid', 'run': '$kparams.exe'}}]

    def reg_pipeline(self):
        return [{'$match': {'name': {'$regex': 'RegDelete|RegSet|RegCreate', '$options': 'i'}, 'kparams.status': 'Success', 'kparams.key_name': {'$ne': None}}}, {'$project': {'_id': 0, 'pid': '$pid', 'kname': '$kparams.key_name', 'op': '$name'}}] #'cmd': '$ps.cmdline', 'op': '$name'}}]
