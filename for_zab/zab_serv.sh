#!/usr/bin/bash
systemctl restart network
yum install -y http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
yum install -y mariadb mariadb-server
yum install -y zabbix-server-mysql zabbix-web-mysql
systemctl start mariadb
systemctl enable mariadb.service
mysql -e "create database zabbix character set utf8 collate utf8_bin;"
mysql -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zpass';"
mysql -e "UPDATE mysql.user SET Password = PASSWORD('zpass') WHERE User = 'root'"
mysql -e "DROP USER ''@'localhost'"
mysql -e "DROP USER ''@'$(hostname)'"
mysql -e "DROP DATABASE test"
mysql -e "FLUSH PRIVILEGES"

yum install -y zabbix-agent 
systemctl start zabbix-agent
systemctl enable zabbix-agent

zcat /usr/share/doc/zabbix-server-mysql-*/create.sql.gz | mysql -uzabbix -pzpass zabbix

cp /vagrant/for_zab/zabbix_server.conf /etc/zabbix/zabbix_server.conf
cp /vagrant/for_zab/zabbix.conf /etc/httpd/conf.d/zabbix.conf
cp /vagrant/for_zab/vhost.conf /etc/httpd/conf.d/vhost.conf


systemctl enable zabbix-server
systemctl start zabbix-server
systemctl start httpd
systemctl enable httpd

sed -i 's/SELINUX=\(enforcing\|permissive\)/SELINUX=disabled/g' /etc/selinux/config
init 6



