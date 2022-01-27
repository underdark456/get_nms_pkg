import requests
from bs4 import BeautifulSoup
import paramiko
import re
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

nms_input = input('Enter NMS version like "3.5.2.20": ')
print('------------------------------------------------------------')
nms_server_input = input('Enter NMS server ip like "10.10.10.1": ')
print('------------------------------------------------------------')
nms_datapack_dict = {'1': 'nms-datapack_2.0.6.deb',
                     '2': 'nms-datapack_3.0.6_amd64.deb',
                     '3': 'nms-datapack_3.0.7_amd64.deb'}
print('------------------------------------------------------------')
for i,v in nms_datapack_dict.items(): print(i,v)
print('Select a datapack(1,2 or 3): ')
number = str(input())
if number in nms_datapack_dict.keys():
    datapack_version = nms_datapack_dict[number]
    print(f'selected {datapack_version}')
else:
    print('Something gone wrong, type correct number from the list')

datapack_check = 'dpkg -l | grep nms-datapack'
datapack_remove = 'dpkg --purge nms-datapack'
datapack_download = f'wget http://pkg.comtechtechnologies.ru/datapack/{datapack_version}'
datapack_install = f'dpkg --install {datapack_version}'
datapack_sh = '/datapack.sh'

if '3.5' in nms_input:
    url = f'http://pkg.comtechtechnologies.ru/nms-dist/3.5.0/nms-dist-{nms_input}.tar.gz'
    nms_download_install = f'wget {url} && tar -zxf nms-dist-{nms_input}.tar.gz'
elif '3.6' in nms_input:
    url = f'http://pkg.comtechtechnologies.ru/nms-dist/3.6/nms-dist-{nms_input}.tar.gz'
    nms_download_install = f'wget {url} && tar -zxf nms-dist-{nms_input}.tar.gz'
elif '3.7' in nms_input:
    url = f'http://pkg.comtechtechnologies.ru/nms-dist/3.7/nms-dist-{nms_input}.tar.gz'
    nms_download_install = f'wget {url} && tar -zxf nms-dist-{nms_input}.tar.gz'

def connect_to_server():
    ip = nms_server_input
    port = 22
    username = 'user'
    password = '1'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(datapack_check)
    outlines = stdout.readlines()
    resp = ''.join(outlines)
    print(resp)
    if 'nms-datapack' in resp:
        print('Datapack installed. Removing and going on.')
        stdin, stdout, stderr = ssh.exec_command(f'{datapack_remove} && {datapack_download_install}')
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)
        stdin, stdout, stderr = ssh.exec_command(nms_download_install)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)
    else:
        print(f'No datapack installed. Download and Install {datapack_version} and NMS {nms_input}.')
        stdin, stdout, stderr = ssh.exec_command(f'{datapack_download} && {datapack_install} && {datapack_sh}')
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)
        stdin, stdout, stderr = ssh.exec_command(f'{datapack_install} && {datapack_sh}')
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)


connect_to_server()
