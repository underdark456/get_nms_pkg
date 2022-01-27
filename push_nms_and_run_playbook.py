import re
import paramiko
import logging
import time

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

nms_version = str(input('nms_version: '))

d = {'3.5.2_all          ': '2.0.6',
'3.6_until_3.6.0.53 ': '3.0.7',
'3.6_since_3.6.0.54 ': '3.0.8',
'3.7_until_3.7.0.33 ': '3.0.7',
'3.7_since_3.7.0.34 ': '3.0.8',
}
for k, v in d.items():
    print(k,v)

datapack_version = str(input('datapack_version: '))
server = str(input('What is the server ip?: ' ))

link_dict = {'3.5' : 'http://pkg.comtechtechnologies.ru/nms-dist/3.5.0/nms-dist-',
             '3.6' : 'http://pkg.comtechtechnologies.ru/nms-dist/3.6/tick5/nms-dist-',
             '3.7' : 'http://pkg.comtechtechnologies.ru/nms-dist/3.7/tick5/nms-dist-',
             'datapack' : 'http://pkg.comtechtechnologies.ru/datapack/nms-datapack_'
             }

nms_pattern = re.search(r'^...', nms_version)
print(nms_pattern.group(0))
if nms_pattern.group(0) in link_dict.keys():
    nms_link = link_dict[nms_pattern.group(0)] + nms_version + '.tar.gz'
    print(nms_link)
    if datapack_version == '2.0.6':
        pass
    else:
        print(link_dict['datapack'] + datapack_version + '_amd64.deb')
else:
    print('Something go wrong')


private_key = r"C:\Users\ish\OneDrive - Comtech Telecommunications Corp\Work\new_keys\private_openssh"
k = paramiko.RSAKey.from_private_key_file(private_key, password='H9a#Pq7)')
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(hostname='10.56.13.22', port='22', username='ishavrov', pkey=k)

playbook_dict = { '3.5': 'nms_35.yml',
                  '3.6': 'nms_36.yml',
                  '3.7': 'nms_37.yml',}

playbook = playbook_dict[nms_pattern.group(0)]
print(playbook)

nms_ver_sed = F'sed -i -E "s#nms-dist-.......?[[:digit:]]#nms-dist-{nms_version}#g" /home/ishavrov/playbooks/{playbook}'
stdin, stdout, stderr = c.exec_command(nms_ver_sed)

for line in stdout.read().splitlines():
    print(line)

if datapack_version == '2.0.6':
    pass
else:
    datapack_ver_sed = F'sed -i -E "s#(deb:[^[:digit:]]*)(.....)(.*)#\\1{datapack_version}\\3#g" /home/ishavrov/playbooks/{playbook}'
    stdin, stdout, stderr = c.exec_command(datapack_ver_sed)
    for line in stdout.read().splitlines():
        print(line)

ansible_run = F'ansible-playbook /home/ishavrov/playbooks/{playbook} -e "target={server} ansible_become_pass=1 ansible_ssh_user=user" -i {server},'
stdin, stdout, stderr = c.exec_command(ansible_run, get_pty=True)
for line in stdout.read().splitlines():
    print(line)


c.close()
