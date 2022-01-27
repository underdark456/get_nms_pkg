import requests
import time


def traf_gen(remote_ip,vlan,pps_1,pps_2,pkt_1,pkt_2):
    local_ip_list = list(map(str, input("Enter local ip addresses(through space): ").split()))
    print(local_ip_list)
    for i in local_ip_list:
        while True:
            try:
                requests.get(f'http://{i}/cw43?db=1&di=0&ic={remote_ip}&Ij=%3A%3A&df={vlan}&dd={pps_1}&dg={pps_2}&de={pkt_1}&dh={pkt_2}&ta=Apply', timeout=(60, 3)).raise_for_status()
            except requests.exceptions.RequestException as err:
                print("Нет ответа    " + str(i))
                time.sleep(5)
                continue
            break

traf_gen('1.1.1.1','101','300','300','300','300')

