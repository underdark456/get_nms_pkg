from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import logging
import paramiko

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

url_list = {'3.5':'http://pkg.comtechtechnologies.ru/nms-dist/3.5.0/',
            '3.6':'http://pkg.comtechtechnologies.ru/nms-dist/3.6/tick5/',
            '3.7':'http://pkg.comtechtechnologies.ru/nms-dist/3.7/tick5/'}


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_dataList(url):#Получаем лист с данными релиза и даты
    data_list = []
    for a in get_soup(url).find_all('a'):
        data_list.append(a.text.split() + re.findall(r'..-...-.... ..:..', a.next_sibling.strip()))
    return data_list

def get_sorted_timestamps(url):#Выделяем лист timestamp'ов с url'a и сортируем
    timestamps = re.findall(r'..-...-.... ..:..', get_soup(url).get_text())
    timestamps.sort(key=lambda x: time.mktime(time.strptime(x, '%d-%b-%Y %H:%M')))
    return timestamps

def time_stamps(url,fileName):#Читаем файл с предыдущей датой и приводим дату с файла и последнюю в листе к одному формату
    try:
        f = open(f"{fileName}.txt", "r")
    except FileNotFoundError:
        f = open(f"{fileName}.txt", "a+")
    content = f.read()
    # timestamp = datetime.strptime(get_sorted_timestamps(url)[-1], "%d-%b-%Y %H:%M")
    # file_timestamp = datetime.strptime(content, "%d-%b-%Y %H:%M")
    # str(timestamp), str(file_timestamp)
    return content,get_sorted_timestamps(url)[-1]

def find_index(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return ([mylist.index(sub_list), sub_list.index(char)])
    raise ValueError("'{char}' is not in list".format(char=char))

def find_index(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return ([mylist.index(sub_list), sub_list.index(char)])
    raise ValueError("'{char}' is not in list".format(char = char))

def main_condition(url,fileName,nms_ver):

    list_date = datetime.strptime(time_stamps(url,fileName)[1],"%d-%b-%Y %H:%M")
    file_date = datetime.strptime(time_stamps(url,fileName)[0],"%d-%b-%Y %H:%M")
    print(list_date)
    print(file_date)
    if file_date > list_date:
        print('no new version')
    else:
        latestReleaseDate = find_index(get_dataList(url), get_sorted_timestamps(url)[-1])
        print(f"There is a new version with date {get_sorted_timestamps(url)[-1]}" + "\nGetting the link...")
        tempList = get_dataList(url)[latestReleaseDate[0]]
        link = url + str(tempList[0])
        print(link)
        #Пишем текущую дату в файл
        f = open(f"{fileName}.txt", "w")
        f.write(datetime.now().strftime("%d-%b-%Y %H:%M"))
        f.close()
        #Подключаемся к серверу и меняем урл на новый
        private_key = r"C:\Users\ish\OneDrive - Comtech Telecommunications Corp\Work\new_keys\private_openssh"
        k = paramiko.RSAKey.from_private_key_file(private_key, password='H9a#Pq7)')
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname='10.56.13.22', port='22', username='ishavrov', pkey=k)
        nms_name = re.match(r'\w{3}-\w{4}-........', str(tempList[0]))
        nms_name_result = nms_name.group(0)
        print(nms_name_result)
        # stdin, stdout, stderr = c.exec_command(f'''sed -i 's|http.*.gz|{link}|' /home/ishavrov/playbooks/nms_36.yml''')
        stdin, stdout, stderr = c.exec_command('''sed -i -E "s/(\w{3}-\w{4}-........)/%s/g" /home/ishavrov/playbooks/nms_3%s.yml''' % (nms_name_result, nms_ver))
        print(stdout.readlines())
        c.close()

main_condition(url_list['3.5'],'3.5','5')



