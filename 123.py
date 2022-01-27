import glob
import magic
import re

files = glob.glob('c')
file_dict = dict(zip(files, file_types))

uncompressed = []

def file_identifier(file):
    for key, value in file_dict.items():
        if file in value:
            uncompressed.append(key)

while file_identifier('text/plain'):
    file_identifier('text/plain') in file_dict

pattern = '2022-01-18'
new_file = open('./ERROR.txt', 'w', encoding='utf8')

for txt_files in uncompressed:
    with open(txt_files, 'r', encoding='utf8') as text_file:
        for line in text_file:
            if re.search(pattern, line):
                new_file.write(line)