from cryptography.fernet import Fernet
from os.path import isfile, join
from os import listdir
import json
from bankingDefs import OperationsAccount, Encryption

# main
OperationsAccount()


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


# Example
data = {}
data['key'] = 'value'

#writeToJSONFile('history', 'file-name', data)

onlyfiles = [f
             for f in listdir("./history")
             if isfile(join("./history", f))]
onlyFilesStrings = [files.replace(".json", "")
                    for files in onlyfiles
                    ]

print(onlyFilesStrings)


with open("key.key", "rb") as keyFile:
    key = keyFile.read()
    f = Fernet(key)

print(f.decrypt(bytes(onlyFilesStrings[0].strip("'").replace(
    "b'", ""), encoding="UTF-8-sig")).decode(encoding="UTF-8-sig"))

encryption = Encryption()

print(encryption.decrypt_list(onlyFilesStrings))
