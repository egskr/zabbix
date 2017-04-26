#! /usr/bin/env python
import os, requests, json
from requests.auth import HTTPBasicAuth

zabbix_server = "192.168.33.75"
zabbix_api_admin_name = "Admin"
zabbix_api_admin_password = "zabbix"
zabbix_agent = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | \
grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| grep 192").readline()

host_name = os.popen('hostname').readline()
host_group_name = "CloudHosts"
custom_template = "Eg_Custom_Template"

def post(request):
    headers = {'content-type': 'application/json'}
    return requests.post(
        "http://" + zabbix_server + "/api_jsonrpc.php",
         data=json.dumps(request),
         headers=headers,
         auth=HTTPBasicAuth(zabbix_api_admin_name, zabbix_api_admin_password)
    )

auth_token = post({
     "jsonrpc": "2.0",
     "method": "user.login",
     "params": {
          "user": zabbix_api_admin_name,
          "password": zabbix_api_admin_password
      },
     "auth": None,
     "id": 0}
 ).json()["result"]


class Creation(object):
    def host_group_add(self):
        post({
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": host_group_name
            },
            "auth": auth_token,
        })

    def register_host(self):
        post({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host_name,
                "templates": [{
                    "templateid": Definition().template_id_def(custom_template)[0]['templateid']
                }],
                "interfaces": [{
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": zabbix_agent,
                    "dns": "",
                    "port": "10050"
                }],
                "groups": [
                    {"groupid": Definition().group_id_def(host_group_name)[0]['groupid']
                     }],
            },
            "auth": auth_token,
            "id": 1
        })


class Definition(object):
    def group_id_def(self, group_name):
        result = post({
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": group_name,
            }
        },
        "auth": auth_token,
        "id": 1
        }).json()["result"]
        return result

    def template_id_def(self, custom_template):
        result = post({
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {            "output": "extend",
            "filter": {
                "host": [custom_template]
            }
        },
        "auth": auth_token,
        "id": 1
        }).json()["result"]
        return result


class Checking(object):
    def host_group_checking(self):
        result = post({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [host_group_name]
                }
            },
            "auth": auth_token,
            "id": 1
        }).json()["result"]
        return result

    def template_checking(self):
        result = post({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [custom_template]
                }
            },
            "auth": auth_token,
            "id": 1
        }).json()["result"]
        return result


if (Checking().host_group_checking()) == []:
  Creation().host_group_add()

if (Checking().template_checking()) != []:
    Creation().register_host()