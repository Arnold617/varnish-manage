import requests, socket, hashlib, time, subprocess, json
from jinja2 import Template
import logging


base_url = "http://domain.varnish.com"
ClientAPi_url = base_url + "/api/clientApi.json"
MasterApi_url = base_url + "/api/masterApi.json"
ipAddress_url = base_url + "/ipAddress/"

user = "username"
key = "IC@Dr4F2jskEkuz-"
ts = str(int(time.time()))

check_cmd = "/usr/sbin/varnishd -Cf /etc/varnish/default.vcl"
reload_cmd = "/usr/sbin/varnish_reload_vcl"


def logs(message):
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="/var/log/varnish_client.log",
                        level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)
    logging.info(message)
#    logging.warning(message)
#    logging.error(message)
#    logging.critical(message)
    return True


def sign():
    md5_sum = user+key+ts
    md5 = hashlib.md5(bytes(md5_sum, encoding='utf-8'))
    md5 = md5.hexdigest()
    return md5


def getData(url):
    _sign = sign()
    headers = {
        'user': user,
        'ts': ts,
        'sign': _sign,
        'Content-Type': 'application/json'
    }
    result = requests.get(url, headers=headers)
    return result.json()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def return_data(url, data):
    _sign = sign()
    headers = {
        'user': user,
        'ts': ts,
        'sign': _sign,
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, data, headers=headers)
    return response


def post_data(url, data):
    _sign = sign()
    headers = {
        'user': user,
        'ts': ts,
        'sign': _sign,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data, headers=headers)
    return response


def check_reload(cmd):
    result = subprocess.getstatusoutput(cmd)[0]
    return result


def disposal_Data(url):
    node_list = getData(ipAddress_url).get('data') # 获取ipList
    local_ip = get_host_ip()
    for host in node_list:
        if local_ip == host.get('ip'):
            if host.get('status') == 1:
                ID = host.get('id')
                data = getData(url)
                data = data.get('data')  # 是一个list，每个元素包含一个站点的所有信息x
                domain_list = []
                # 站点数据重组后：obj_data = [{'name':'11', 'ip':'1.1.1.1'},{'name':'22', 'ip':'2.2.2.2'}]
                for site_info in data:
                    obj_data = []
                    sum = 0
                    varnish = site_info.get('node').get('varnish').split(',')
                    local_ip = get_host_ip()
                    if local_ip in varnish:
                        status = site_info.get('status')
                        domain = site_info.get('domain')
                        domain_list.append(domain)
                        if status == 1:
                            ip_address = site_info.get('ip_address').split(',')
                            backup_name = domain.replace('.', '_')
                            if backup_name[0].isdigit():
                                backup_name = 'u'+backup_name
                            print(backup_name)

                            domain_name = backup_name.upper()
                            template = site_info.get('template')
                            for host in ip_address:
                                backup = {}
                                sum += 1
                                backup['name'] = backup_name + '_' + str(sum)
                                backup['ip'] = host
                                obj_data.append(backup)
                            # 注意: 子站点下线后, 文件需要删除
                            temp = Template(template)
                            with open('/etc/varnish/conf.d/'+domain+'.vcl', 'w+') as config:
                                config.write(temp.render(backend_obj=obj_data,
                                                         domain_name=domain_name))
                return domain_list,ID,local_ip


# [{'domain':'www.com','domain_name':'WWW_COM'},{'domain':'12.com,'domain_name':'12_COM'}]
def disposal_master(domain_list, url):
    backup_obj = []
    data = getData(url)
    try:
        data = data.get('data')[0]
    except:
        data = data.get('data')
        print(data)
    status = data.get('status')
    template = data.get('content')
    item_obj = data.get('masterItem').get('content')
    print(data)

    if status == 1:
        for domain in domain_list:
            backup = {}
            backup['domain'] = domain
            if domain[0].isdigit():
                domain = 'u'+domain
            backup['domain_name'] = domain.replace('.', '_').upper()
            backup_obj.append(backup)
        _temp = Template(template)
        with open('/etc/varnish/default.vcl', 'w+') as master_config:
            master_config.write(_temp.render(backend_obj=backup_obj,
                                            masterItem_obj=item_obj))


if __name__ == '__main__':
    # 如果ip的status为0,不需要check
    message = "not update"
    try:
        domain_list,ID,local_ip = disposal_Data(ClientAPi_url)
    except TypeError as e:
        # print("无更新")
        message = "无更新"
    else:
        disposal_master(domain_list, MasterApi_url)
        status = 0
        if check_reload(check_cmd) == 0:
            if check_reload(reload_cmd) == 0:
                message = "reload success !!!"
            else:
                status = 2
                message = "reload fail !!!"
        else:
            status = 2
            message = "check fail !!!"

        # 用patch方法回写库改状态，修改ipaddress的更新状态
        host_url = ipAddress_url + str(ID)
        update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        data = { 'status': 0, 'updated_at': update_time}
        return_data(host_url, json.dumps(data))

    result = logs(message)
    print(result)
