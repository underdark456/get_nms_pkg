import paramiko
def ssh_connect_update():
    private_key = r"C:\Users\ish\OneDrive - Comtech Telecommunications Corp\Work\new_keys\private_openssh"
    k = paramiko.RSAKey.from_private_key_file(private_key, password='H9a#Pq7)')
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = '10.56.13.22', port='22', username = 'ishavrov', pkey=k)

    stdin, stdout, stderr = c.exec_command('''sed -i 's|http.*.gz|http://pkg.comtechtechnologies.ru/nms-dist/3.5.0/nms-dist-3.5.2.25.tar.gz|' /home/ishavrov/playbooks/nms_35.yml''')
    print(stdout.readlines())
    c.close()

result = ssh_connect_update()
print(result)
