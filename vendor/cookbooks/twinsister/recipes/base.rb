include_recipe "apt"
include_recipe "locale"
include_recipe "nginx"
include_recipe "python"

ENV['LANGUAGE'] = ENV['LANG'] = ENV['LC_ALL'] = "en_US.UTF-8"
include_recipe "postgresql::server"

include_recipe "nodejs::install_from_package"
include_recipe "supervisor"

# venv_root = "#{node['twinsister']['app_root']}/env"
# venv_pip = "#{venv_root}/bin/pip"
# home =
# home = "/home/#{node['twinsister']['user']}"

# virtualenv
python_virtualenv "#{node['twinsister']['app_root']}/env" do
  action :create
  owner node['twinsister']['user']
end

# pillow requirements
%w(libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev).each do |pkg|
  package pkg do
    action :install
  end
end

apt_package "memcached"

# python requirements
execute "python_requirements" do
  command "env/bin/pip install -r requirements.txt"
  cwd node['twinsister']['app_root']
end

# less
execute "npm install -g less"

# create db role and db if they don't exist
db_user = node['twinsister']['db']['user']
db_name = node['twinsister']['db']['name']

execute "create_db_role" do
  command "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='#{db_user}'\" | grep -q 1 || createuser -SDR #{db_user}"
  user "postgres"
end

execute "create_db" do
  command "psql -lqt | cut -d \\| -f 1 | grep -wq #{db_name} || createdb -O #{db_user} #{db_name}"
  user "postgres"
end

# nginx conf
template "/etc/nginx/sites-available/twinsister" do
  source "nginx.erb"
  owner node['nginx']['user']
  group node['nginx']['user']
  variables({app_root: node['twinsister']['app_root']})
end

# supervisor
template "/etc/supervisor.d/twinsister.conf" do
  source "supervisor.erb"
  variables({app_root: node['twinsister']['app_root'],
    user: node['twinsister']['user']})
end

service "supervisor" do
  action :restart
end
