#!/usr/bin/bash

systemctl restart network
rpm -ivh http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
yum install -y zabbix-agent epel-release net-tools

firewall-cmd --add-port=10050/tcp --permanent
firewall-cmd --add-port=10051/tcp --permanent

cp /vagrant/for_zab/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf
sed -i "s/XXXX/$(hostname)/g" /etc/zabbix/zabbix_agentd.conf

yum -y install python-pip
pip install requests
pip install --upgrade pips

chmod +x /vagrant/for_zab/discovery_host.py
/vagrant/for_zab/discovery_host.py

systemctl start zabbix-agent
systemctl enable zabbix-agent

sed -i 's/SELINUX=\(enforcing\|permissive\)/SELINUX=disabled/g' /etc/selinux/config
init 6
