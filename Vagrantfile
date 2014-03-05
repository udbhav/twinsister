# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  config.vm.network :forwarded_port, host: 8001, guest: 80

  kishore_location = ENV['KISHORE_LOCATION'] ||= "/Users/foucault/Sites/kishore/django-kishore/kishore"
  config.vm.synced_folder kishore_location, "/home/vagrant/kishore"

  config.omnibus.chef_version = :latest
  config.berkshelf.enabled = true

  config.vm.provision "chef_solo" do |chef|
    chef.add_recipe "apt"
    chef.add_recipe "nginx"
    chef.add_recipe "python"
    chef.add_recipe "postgresql::server"
    chef.add_recipe "nodejs::install_from_package"
    chef.add_recipe "supervisor"
    chef.add_recipe "rvm::user"
    chef.add_recipe "twinsister"

    chef.json = {
      "postgresql" => {
        "password" => { "postgres" => "postgres" }
      },
      "rvm" => {
        "user_installs" => [{"user" => "vagrant"}],
        "vagrant" => {
          "system_chef_client" => "/opt/chef/bin/chef-client",
          "system_solo_client" => "/opt/chef/bin/chef-solo"
        },
      },
    }
  end
end
