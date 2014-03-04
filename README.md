Twin Sister
-----------

Installation
------------

For development, use [Vagrant](http://vagrantup.com) with the Chef Omnibus and Berkshelf plugins.

    vagrant plugin install vagrant-omnibus
    vagrant plugin install vagrant-berkshelf
    vagrant up
    vagrant ssh
    source env/bin/activate && cd /vagrant/src
    gunicorn -b unix:/tmp/gunicorn.sock twinsister.wsgi:application

To setup a production server on Rackspace (make sure you've setup the .chef directory):

    knife rackspace server create -r 'role[webserver]' --server-name SERVER_NAME \
    --node-name tstest --image 80fbcb55-b206-41f9-9bc2-2dd7aac6c061 --flavor 2 \
    --rackspace-region iad
