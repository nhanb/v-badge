# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version ">= 1.7.0"

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"
  config.vm.network "private_network", ip: "192.168.77.2"

  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder "scripts", "/home/vagrant/scripts", type: "virtualbox"
  config.vm.synced_folder "logs", "/home/vagrant/logs", type: "virtualbox"
  config.vm.synced_folder "vbadge", "/vagrant", type: "virtualbox"

  # Disable the new default behavior introduced in Vagrant 1.7, to
  # ensure that all Vagrant machines will use the same SSH key pair.
  # See https://github.com/mitchellh/vagrant/issues/5005
  config.ssh.insert_key = false

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      'webservers' => ['default']
    }
    ansible.verbose = "v"
    ansible.playbook = "ansible/site.yml"
    ansible.sudo = true
  end
end
