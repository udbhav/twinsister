include_recipe "twinsister::base"

# temporary kishore dev stuff
execute "kishore_symlink" do
  command "ln -sf /home/vagrant/kishore /vagrant/env/lib/python2.7/site-packages/kishore"
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

execute "/vagrant/env/bin/pip install ipython"

# ruby
# rvm_shell "bundle_install" do
#   user "vagrant"
#   code "bundle install"
#   cwd "/vagrant/"
# end

# supervisor
execute "supervisor" do
  command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
    ln -sf /vagrant/cookbooks/twinsister/files/default/supervisor.conf
    /etc/supervisor.d/twinsister.conf
  EOS
end

service "supervisor" do
  action :restart
end

# django init stuff
# execute "django_init" do
#   command <<-EOS.gsub(/^[\s\t]*/, '').gsub(/[\s\t]*\n/, ' ').strip
#     /vagrant/env/bin/python /vagrant/src/manage.py syncdb --noinput;
#     /vagrant/env/bin/python /vagrant/src/manage.py migrate;
#     /vagrant/env/bin/python /vagrant/src/manage.py collectstatic -l --noinput
#   EOS
#   user "vagrant"
# end
