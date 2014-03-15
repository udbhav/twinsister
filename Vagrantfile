# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.network :forwarded_port, host: 8001, guest: 80

  kishore_location = ENV['KISHORE_LOCATION'] ||= "/Users/foucault/Sites/kishore/django-kishore/kishore"

  config.vm.synced_folder kishore_location, "/home/vagrant/kishore"
  config.vm.synced_folder ".", "/home/vagrant/mrtwinsister", type: "rsync",
    rsync__exlude: [".git/",".chef/",".vagrant/"]

  config.omnibus.chef_version = :latest

  config.vm.provision "chef_solo" do |chef|
    chef.add_recipe "twinsister::production"

    chef.json = {
      "twinsister" => {
        "user" => "vagrant",
        "app_root" => "/home/vagrant/mrtwinsister",
      },
      "postgresql" => {
        "password" => { "postgres" => "postgres" }
      },
    }
  end
end
