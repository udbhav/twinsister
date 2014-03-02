Twin Sister
-----------

Installation
------------

For development, use [Vagrant](http://vagrantup.com) with the Chef Omnibus and Berkshelf plugins.

    vagrant up
    vagrant ssh
    source env/bin/activate && cd /vagrant/src
    gunicorn -b unix:/tmp/gunicorn.sock twinsister.wsgi:application
