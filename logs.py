import glob
import gzip
import shutil
from pprint import pprint
import magic
import os
import re

def file_type(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime

def _files():
    all_files = [os.path.normpath(i) for i in glob.glob('C:/Users/ish/python_scripts/logs/**', recursive=True)]
    files = []
    for file in all_files:
        if os.path.isfile(file) == True:
            files.append(file)
    file_types = [file_type(file) for file in files]
    file_dict = dict(zip(files, file_types))
    return file_dict

gzip_files = []

def file_identifier(file,_list_):
    for key, value in _files().items():
        if file in value:
            _list_.append(key)

while file_identifier('application/x-gzip',gzip_files):
    file_identifier('application/x-gzip',gzip_files) in _files()



for i in gzip_files:
    with gzip.open(i,'rb') as f_in:
        with open(r'C:\Users\ish\python_scripts\logs\gz.txt','a+b') as f_out:
            shutil.copyfileobj(f_in,f_out)

uncompressed = []
while file_identifier('text/plain',uncompressed):
    file_identifier('text/plain',uncompressed) in _files()

pattern = '2022-01-13'
new_file = open('./pattern.txt', 'w', encoding='utf8')

for files in uncompressed:
    with open(files, 'r', encoding='utf8') as text_file:
        for line in text_file:
            if re.search(pattern, line):
                new_file.write(line)