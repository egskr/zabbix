# -*- mode: ruby -*-
# vi: set ft=ruby :

# YAML config definition
class ConfigData
  def self.yaml_config
    require 'yaml'
    YAML.load_file('vagrant_config.yaml')
  end
end

my_config = ConfigData.yaml_config

  Vagrant.configure("2") do |config|
    config.vm.box = "centos/7"  

    puts "#{my_config.count} hosts configured in Vagrantfile"

    my_config.each do |val|

      config.vm.define val['host'] do |host|
        type = val['host']
        
          host.vm.hostname = type
          host.vm.network "private_network", ip: val['ip']
         
          scr = val['script']
          if scr
            scr.each do |va|
              host.vm.provision 'shell', inline: 
              <<-SHELL
              #{va}
              SHELL
            end
          end

          host.vm.provider "virtualbox" do |v|
            v.memory = val['memory'] if val['memory']
            v.cpus = val['cpu_num'] if val['cpu_num']
          end

      end

    end
  
end

