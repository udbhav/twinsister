Twin Sister
-----------

Installation
------------

For development, use [Vagrant](http://vagrantup.com) with the Chef Omnibus and
Berkshelf plugins.

    vagrant plugin install vagrant-omnibus
    vagrant plugin install vagrant-berkshelf
    vagrant plugin install vagrant-vbguest
    vagrant up

To setup a production server on Rackspace:

    gem install chef
    gem intall knife-rackspace

Set up a .chef directory with a knife.rb file that has the following:

    knife[:rackspace_api_username] = "Your Rackspace API username"
    knife[:rackspace_api_key] = "Your Rackspace API Key"

Run:

    knife rackspace server create -r 'role[webserver]' --server-name SERVER_NAME \
    --node-name NODE_NAME --image 80fbcb55-b206-41f9-9bc2-2dd7aac6c061 --flavor 2 \
    --rackspace-region iad
