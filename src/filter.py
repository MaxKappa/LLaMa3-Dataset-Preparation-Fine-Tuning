import re, json, hashlib
class Filter:
    def __init__(self, hash):
        print("Starting data filtering...")
        self.patterns = [
            r'.*fibratus.*',
            r'.*Fibratus.*',
            r'.*update.*',
            r'.*edge.*',
            r'.*Edge.*',
            r'.*Update.*',
            r'.*WindowsStore.*',
            r'.*Xbox.*',
            r'.*Microsoft.*'
        ]
        self.compiled_patterns = [re.compile(pattern) for pattern in self.patterns]
        self.hash = hash
    def check(self, document, datatype):
        for pattern in self.compiled_patterns:
            try:
                if datatype == "process":
                    if pattern.match(str(document['fname'])): #if pattern.match(str(document['cmd'])) or pattern.match(str(document['fname'])):
                        return False
                elif datatype == "thread":
                    if pattern.match(str(document['run'])):
                        return False
                elif datatype == "reg":
                    if pattern.match(str(document['kname'])): #if pattern.match(str(document['cmd'])) or pattern.match(str(document['kname'])):
                        return False
            except KeyError:
                return False
        return True

    def unique(self, data_list):
        unique_data = list({json.dumps(item) for item in data_list})
        return [json.loads(item) for item in unique_data]
    
    def get_filtered_data(self, data, datatype):
        filtered_data = []
        for document in data:
            if self.check(document, datatype):
                if self.hash == True:
                    filtered_data.append(self.hash_filepath(self.truncate_op(document), datatype))
                else:
                    filtered_data.append(self.truncate_op(document))
        return self.unique(filtered_data)

    def filter_data(self, datatype, path):
        with open(path, 'r') as file_read:
            res = self.get_filtered_data(json.load(file_read), datatype)
        with open(path, 'w') as file_write:
            file_write.write(str(json.dumps(list(res))))
        print(f"File successfully filtered {path}")

    def hash_filepath(self, document, datatype):
        if datatype == 'process':
            document['fname'] = hashlib.sha1(str(document['fname']).encode("UTF-8")).hexdigest()[:10]
        elif datatype == 'reg':
            document['kname'] = hashlib.sha1(str(document['kname']).encode("UTF-8")).hexdigest()[:10]
        return document
    
    def truncate_op(self, document):
        op_diz = {
            'CreateFile': 'C',
            'ReadFile': 'R',
            'DeleteFile': 'D',
            'WriteFile': 'W',
            'RegSetValue': 'SV',
            'RegCreateKey': 'CK',
            'RegDeleteKey': 'DK',
            'RegDeleteValue': 'DV'
        }

        if 'op' in document and document['op'] in op_diz:
            document['op'] = op_diz[document['op']]
        
        return document
