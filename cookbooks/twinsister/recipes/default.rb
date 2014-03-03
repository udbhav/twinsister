# virtualenv
python_virtualenv "/home/vagrant/env" do
  action :create
end

# pillow requirements
%w(libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev).each do |pkg|
  package pkg do
    action :install
  end
end

execute "python_requirements" do
  command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
    /home/vagrant/env/bin/pip install Pillow;
    /home/vagrant/env/bin/pip install -r /vagrant/requirements.txt
  EOS
end

# temporary kishore dev stuff
execute "kishore_symlink" do
  command "ln -sf /home/vagrant/kishore /home/vagrant/env/lib/python2.7/site-packages/kishore"
end

# db
execute "create_db" do
  command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
    psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='vagrant'\" | grep -q 1 ||
    createuser -SDR vagrant;
    psql -lqt | cut -d \\| -f 1 | grep -wq twinsister || createdb twinsister -O vagrant
  EOS
  user "postgres"
end

# nginx
execute "nginx_conf" do
  command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
    ln -sf /vagrant/cookbooks/twinsister/files/default/nginx.conf
    /etc/nginx/sites-enabled/twinsister; /etc/init.d/nginx restart
  EOS
end

execute "/home/vagrant/env/bin/pip install ipython"
execute "npm install -g less"

# django init stuff
execute "django_init" do
  command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
    /home/vagrant/env/bin/python /vagrant/src/manage.py syncdb --noinput;
    /home/vagrant/env/bin/python /vagrant/src/manage.py migrate;
    /home/vagrant/env/bin/python /vagrant/src/manage.py collectstatic -l --noinput
  EOS
  user "vagrant"
end
