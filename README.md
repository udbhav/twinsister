Twin Sister
-----------

Installation
------------

For development, use [Vagrant](http://vagrantup.com) with the Chef Omnibus

    vagrant plugin install vagrant-omnibus
    vagrant plugin install vagrant-vbguest
    gem install librarian-chef
    librarian-chef install
    vagrant up

Setting Up a Production Server
------------------------------

SSH into the server and create the user you'll be using

    adduser udbhav
    adduser udbhav sudo

Upload cookbooks to chef

    knife cookbook upload --all

Bootstrap the server

    knife bootstrap -x root -N nodename -r 'recipe[twinsister::production]' \
    -i ~/.ssh/id_rsa ipaddress

Deploying
---------

Change the run list of the node to twinsister::deploy, and then

    knife ssh 'name:nodename' 'sudo chef-client'